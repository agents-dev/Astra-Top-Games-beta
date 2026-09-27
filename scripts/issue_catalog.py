#!/usr/bin/env python3
"""Extract issue URLs, collect reports, and publish on a credential-isolated runner."""
import argparse
import base64
import io
import json
import os
from pathlib import Path
import re
import subprocess
import time
import urllib.request
import zipfile

import games


def api(path, method='GET', data=None, binary=False):
    command = ['gh', 'api', path, '--method', method]
    if data is not None:
        command += ['--input', '-']
    result = subprocess.run(command, input=json.dumps(data).encode() if data is not None else None,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return result.stdout if binary else json.loads(result.stdout or b'null')


def context():
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    repo = os.environ['GITHUB_REPOSITORY']
    owner = event['issue']['user']['login'].casefold() == event['repository']['owner']['login'].casefold()
    urls, invalid = [], []
    for found in re.findall(r'https?://[^\s<>"`]+', event['issue'].get('body') or ''):
        candidate = found.rstrip('.,;!?:)]}')
        try:
            normalized = games.input_url(candidate)
            if normalized not in urls:
                urls.append(normalized)
        except ValueError as exc:
            invalid.append({'url': candidate, 'reason': str(exc)})
    run = os.environ['GITHUB_RUN_ID']
    return event, repo, owner, urls, invalid, f'https://github.com/{repo}/actions/runs/{run}'


def comment(repo, number, body):
    # Keep every outcome even when an owner supplies a very large batch.
    lines, chunk = body.splitlines(keepends=True), ''
    for line in lines:
        if len(chunk) + len(line) > 50000:
            result = api(f'repos/{repo}/issues/{number}/comments', 'POST', {'body': chunk})
            print('Issue report: ' + result['html_url'], flush=True)
            chunk = ''
        chunk += line[:49000]
    if chunk:
        result = api(f'repos/{repo}/issues/{number}/comments', 'POST', {'body': chunk})
        print('Issue report: ' + result['html_url'], flush=True)


def intake():
    event, repo, owner, urls, invalid, run_url = context()
    allowed = bool(urls) and (owner or len(urls) <= 10)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as out:
        out.write(f"allowed={str(allowed).lower()}\nowner={str(owner).lower()}\n")
    if allowed:
        body = f"## 🎮 Game catalog\n\nI’m on it! This may take 10–30 minutes.\n\n[View the Actions run]({run_url})"
    else:
        reason = 'No supported public HTTP(S) game links found.' if not urls else 'Submit at most 10 distinct URLs per issue. Repository-owner issues have no URL-count limit.'
        body = f'{reason}\n\n[View the Actions run]({run_url})'
    comment(repo, event['issue']['number'], body)


def analyze():
    event, repo, owner, urls, invalid, run_url = context()
    if not urls or (not owner and len(urls) > 10):
        raise ValueError('Issue rejected by intake')
    root = games.WORK / 'issue-catalog'
    root.mkdir(parents=True, exist_ok=True)
    links = root / 'links.txt'
    links.write_text('\n'.join(urls) + '\n')
    return subprocess.call(['python3', str(games.ROOT / 'scripts/games.py'), '--file', str(links),
                            '--summary', str(root / 'result.json'), '--defer-publish'])


def jobs(repo):
    return api(f'repos/{repo}/actions/runs/{os.environ["GITHUB_RUN_ID"]}/attempts/{os.environ.get("GITHUB_RUN_ATTEMPT", "1")}/jobs?per_page=100')['jobs']


def artifact_name():
    return 'catalog-reports-' + os.environ.get('GITHUB_RUN_ATTEMPT', '1')


def wait_reports(repo):
    deadline = time.monotonic() + 285 * 60
    while time.monotonic() < deadline:
        listing = api(f'repos/{repo}/actions/runs/{os.environ["GITHUB_RUN_ID"]}/artifacts?per_page=100')
        found = next((a for a in listing['artifacts'] if a['name'] == artifact_name()), None)
        if found:
            if found['size_in_bytes'] > 32 * 1024 * 1024:
                raise ValueError('Report artifact exceeds 32 MiB')
            blob = api(f'repos/{repo}/actions/artifacts/{found["id"]}/zip', binary=True)
            with zipfile.ZipFile(io.BytesIO(blob)) as archive:
                entry = archive.getinfo('result.json')
                if entry.file_size > 32 * 1024 * 1024:
                    raise ValueError('Report data exceeds 32 MiB')
                return json.loads(archive.read(entry))
        worker = next((j for j in jobs(repo) if j['name'] == 'Analyze games'), None)
        if worker and (worker['status'] == 'completed' or any(
                s['name'] == 'Wait for publication, then hold SSH' and s['status'] == 'in_progress'
                for s in worker.get('steps', []))):
            raise RuntimeError('Analysis produced no report artifact; inspect the Actions logs')
        time.sleep(15)
    raise TimeoutError('Analysis exceeded the publication deadline')


def git(*args, env=None):
    return subprocess.check_output(['git', *args], cwd=games.ROOT, env=env, text=True).strip()


def publish():
    event, repo, owner, urls, invalid, run_url = context()
    statuses = []
    publication, publication_error, branch = '', '', ''
    try:
        result = wait_reports(repo)
        if not isinstance(result, dict) or not isinstance(result.get('items'), list):
            raise ValueError('Invalid analysis result envelope')
        incoming = {item['url']: item for item in result['items'] if isinstance(item, dict) and item.get('url') in urls}
        # The publisher uses its own trusted checkout and renderer, never analysis-side code or paths.
        for url in urls:
            item = incoming.get(url, {'status': 'failed', 'reason': result.get('error') or 'No result returned'})
            try:
                if item.get('status') == 'ready':
                    report = item['report']
                    if len(json.dumps(report)) > 1024 * 1024:
                        raise ValueError('Report exceeds 1 MiB')
                    record = games.publish_report(report, url, {'issue': event['issue']['number'], 'run_url': run_url})
                    statuses.append({'url': url, **record})
                else:
                    reason = str(item.get('reason') or item.get('status') or 'Analysis failed')[:2000]
                    existing = games.destination({'repository_url': url if 'github.com/' in url and url.startswith('https://github.com/') else ''}, url)
                    replaced = (existing / 'readme.json').exists()
                    status = 'replacement_failed' if replaced else item.get('status', 'failed')
                    statuses.append({'url': url, 'status': status, 'reason': reason})
            except (ValueError, OSError, KeyError, TypeError) as exc:
                existing = games.destination({'repository_url': ''}, url)
                status = 'replacement_failed' if (existing / 'readme.json').exists() else 'failed'
                statuses.append({'url': url, 'status': status, 'reason': str(exc)[:2000]})
        games.rebuild()
        git('add', '--', 'games', 'README.md')
        if git('diff', '--cached', '--name-only'):
            branch = f'codex/issue-{event["issue"]["number"]}-{os.environ["GITHUB_RUN_ID"]}-{os.environ.get("GITHUB_RUN_ATTEMPT", "1")}'
            git('switch', '-c', branch)
            git('config', 'user.name', 'github-actions[bot]')
            git('config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com')
            message = (f'Update game catalog from issue #{event["issue"]["number"]}\n\n'
                'Analyze the submitted public links with OpenCode. Publish validated game reports in the shared catalog; '
                'replace matching entries only after validation and retain previous entries on analysis failure. '
                'Keep source-unavailable games with an empty repository_url and preserve input evidence links.\n\n'
                f'Verification: revalidate reports and render catalog pages on a separate trusted publishing runner. '
                f'Inspect the per-game issue report and Actions records for evidence gaps and failures.\n\n'
                f'Actions: {run_url}\nChat-ID: 01a0e073-33c0-7313-8d6f-f99664a22049')
            git('commit', '-m', message)
            env = os.environ.copy()
            encoded = base64.b64encode(('x-access-token:' + os.environ['GH_TOKEN']).encode()).decode()
            env.update(GIT_CONFIG_COUNT='1', GIT_CONFIG_KEY_0='http.https://github.com/.extraheader',
                       GIT_CONFIG_VALUE_0='AUTHORIZATION: basic ' + encoded)
            git('push', 'origin', f'HEAD:refs/heads/{branch}', env=env)
            publication = f'https://github.com/{repo}/tree/{branch}'
            print('Published branch: ' + publication, flush=True)
            try:
                pr = api(f'repos/{repo}/pulls', 'POST', {'title': f'Update game catalog from issue #{event["issue"]["number"]}',
                    'head': branch, 'base': event['repository']['default_branch'],
                    'body': f'Process game links from #{event["issue"]["number"]}.\n\n[Analysis run]({run_url})\n\nReview additions, replacements, and evidence before merging.'})
                publication = pr['html_url']
                print('Created PR: ' + publication, flush=True)
            except Exception as exc:
                publication_error = 'PR creation failed; use the published branch. ' + str(exc)[:500]
    except Exception as exc:
        publication_error = str(exc)[:1000]
        reported = {s['url'] for s in statuses}
        statuses += [{'url': u, 'status': 'failed', 'reason': publication_error} for u in urls if u not in reported]
    body = ['## Game catalog results', '', f'[View the Actions run]({run_url})', '']
    if publication:
        body += [f'[Open the PR or published branch]({publication})', '']
    elif not publication_error:
        body += ['No catalog changes to publish.', '']
    if publication_error:
        body += ['Publication error: ' + games.markdown(publication_error), '']
    for item in statuses:
        status = item['status']
        if status in ('added', 'replaced'):
            label = status.capitalize() if publication else f'{status.capitalize()} locally; publication failed'
            page = f'https://github.com/{repo}/blob/{branch}/{item["output"]}/README.md' if publication else run_url
            source = ''
            report = json.loads((games.ROOT / item['output'] / 'readme.json').read_text())
            if not report['repository_url']:
                source = ' — GitHub source unavailable'
            body.append(f'- **{label}**: [{games.markdown(item["title"])}]({page}){source}')
        else:
            label = {'not_game': 'Not a game', 'inaccessible': 'Inaccessible',
                     'replacement_failed': 'Replacement failed—previous version retained'}.get(status, 'Failed')
            body.append(f'- **{label}**: {games.markdown(item["url"])} — {games.markdown(item.get("reason", ""))}')
    body += [f'- **Invalid link**: {games.markdown(i["url"])} — {games.markdown(i["reason"])}' for i in invalid]
    body += ['', 'Inspect the Actions records for complete analysis logs.']
    comment(repo, event['issue']['number'], '\n'.join(body))
    if publication_error:
        raise RuntimeError(publication_error)


def hold():
    _, repo, owner, _, _, _ = context()
    if not owner:
        return
    deadline = time.monotonic() + 30 * 60
    while time.monotonic() < deadline:
        try:
            publisher = next((j for j in jobs(repo) if j['name'] == 'Publish catalog PR'), None)
            if publisher and publisher['status'] == 'completed':
                break
        except Exception as exc:
            print(f'Waiting for publisher status: {exc}', flush=True)
        time.sleep(15)
    print('Publication phase ended. Keep this worker and SSH tunnel alive for 30 minutes.', flush=True)
    with open(os.environ['GITHUB_STEP_SUMMARY'], 'a') as out:
        out.write('\n## SSH debug hold\nKeep this worker available for 30 minutes after publication.\n')
    time.sleep(1800)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['intake', 'analyze', 'publish', 'hold'])
    args = parser.parse_args()
    raise SystemExit(globals()[args.command]() or 0)
