#!/usr/bin/env python3
"""Analyze public game links, replace matching reports, and rebuild one shared catalog."""

import argparse
import concurrent.futures
from datetime import datetime, timezone
import fcntl
import html
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
from urllib.parse import quote, urlsplit

import test_oc


ROOT = Path(__file__).resolve().parent.parent
GAMES = ROOT / 'games'
WORK = ROOT / 'work'


def game_url(value):
    parsed = urlsplit(value.strip())
    parts = [part for part in parsed.path.strip('/').split('/') if part]
    if parsed.scheme != 'https' or parsed.netloc.lower() != 'github.com' or parsed.query or parsed.fragment:
        raise ValueError(f'Not a plain HTTPS GitHub game link: {value}')
    if len(parts) < 2 or not all(re.fullmatch(r'[A-Za-z0-9_.-]+', p) for p in parts):
        raise ValueError(f'Invalid GitHub game link: {value}')
    owner, repo = parts[:2]
    repo = repo.removesuffix('.git')
    if not owner or not repo:
        raise ValueError(f'Invalid GitHub game link: {value}')
    if len(parts) > 2:
        if len(parts) < 4 or parts[2] != 'tree':
            raise ValueError(f'Use a repository URL or /tree/<branch>/<game-directory>: {value}')
        game_parts = parts[4:]
    else:
        game_parts = []
    if any(p in ('.', '..') for p in game_parts):
        raise ValueError(f'Unsafe game directory: {value}')
    normalized = f'https://github.com/{owner}/{repo}'
    if len(parts) > 2:
        normalized += '/tree/' + '/'.join(parts[3:])
    directory = GAMES / f'{owner}--{repo}'
    if game_parts:
        directory = directory.joinpath(*game_parts)
    return normalized, directory


def input_url(value):
    parsed = urlsplit(value.strip())
    if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError('Require a public HTTP(S) URL without credentials')
    host = parsed.hostname.lower()
    if host == 'localhost' or host.endswith(('.localhost', '.local', '.internal')) or '.' not in host:
        raise ValueError('Require a public host')
    try:
        address = ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        if not address.is_global:
            raise ValueError('Require a public address')
    if parsed.port not in (None, 80, 443):
        raise ValueError('Require a standard HTTP(S) port')
    if host == 'github.com':
        return game_url(value)[0]
    return parsed._replace(fragment='', netloc=host if parsed.port is None else parsed.netloc).geturl()


def destination(data, submitted):
    repo = data.get('repository_url', '')
    for path in sorted(GAMES.rglob('readme.json')) if GAMES.exists() else []:
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
            continue
        try:
            old = json.loads(path.read_text())
            if (repo and old.get('repository_url', '').lower() == repo.lower()) or submitted in old.get('links', []):
                return path.parent
        except (ValueError, OSError):
            continue
    if repo:
        return game_url(repo)[1]
    return GAMES / ('web--' + hashlib.sha256(submitted.encode()).hexdigest()[:20])


def checked_report(data, submitted):
    validate(data, submitted if urlsplit(submitted).hostname == 'github.com' else None)
    data = dict(data)
    data['links'] = list(dict.fromkeys([submitted] + [u for u in data['links'] if safe_url(u)]))
    return data


def publish_report(data, submitted, metadata=None):
    data = checked_report(data, submitted)
    directory = destination(data, submitted)
    if any(p.is_symlink() for p in [directory, *directory.parents]):
        raise ValueError('Refuse symlink catalog destination')
    status = 'replaced' if (directory / 'readme.json').exists() else 'added'
    if status == 'replaced':
        previous = json.loads((directory / 'readme.json').read_text())
        data['links'] = list(dict.fromkeys(data['links'] + [u for u in previous.get('links', []) if safe_url(u)]))
    rendered = game_readme(data)
    write_atomic(directory / 'readme.json', json.dumps(data, indent=2, ensure_ascii=False) + '\n')
    write_atomic(directory / 'README.md', rendered)
    record = {'added_at': datetime.now(timezone.utc).isoformat(), 'source_url': submitted,
              'output': str(directory.relative_to(ROOT)), 'status': status, 'title': data['title'],
              'rating_score': data['rating']['score'],
              'screenshot_based_score': None if data['screenshot_based_score'] is None else data['screenshot_based_score']['score']}
    record.update(metadata or {})
    with (GAMES / 'added.jsonl').open('a', encoding='utf-8') as ledger:
        ledger.write(json.dumps(record, ensure_ascii=False) + '\n')
    return record


def markdown(value):
    return re.sub(r'([\\`*_{}\[\]<>|])', r'\\\1', str(value).replace('\n', ' '))


def safe_url(value):
    if not isinstance(value, str):
        return None
    parsed = urlsplit(value)
    if parsed.scheme not in ('http', 'https') or not parsed.netloc:
        return None
    return quote(value, safe=':/?#[]@!$&\'*+,;=%-._~')


def score(value, name, nullable=False):
    if value is None and nullable:
        return None
    if not isinstance(value, dict):
        raise ValueError(f'{name} must contain an integer score')
    number = value.get('score')
    if type(number) is not int or not 0 <= number <= 100:
        raise ValueError(f'{name}.score must be an integer between 0 and 100')
    return number


def validate(data, expected_url=None):
    if not isinstance(data, dict):
        raise ValueError('Report must be a JSON object')
    url = data.get('repository_url')
    if not isinstance(url, str):
        raise ValueError('repository_url must be a GitHub URL or an empty string')
    normalized = game_url(url)[0] if url else ''
    if expected_url and normalized != expected_url:
        raise ValueError(f'Report URL does not match input: {url}')
    if not isinstance(data.get('title'), str) or not data['title'].strip():
        raise ValueError('Report must have a title')
    score(data.get('rating'), 'rating')
    score(data.get('screenshot_based_score'), 'screenshot_based_score', nullable=True)
    if not isinstance(data.get('screenshots'), list):
        raise ValueError('Report must have a screenshots list')
    for shot in data['screenshots']:
        if not isinstance(shot, dict) or not safe_url(shot.get('url')):
            raise ValueError('Each screenshot must have an HTTP(S) URL')
    for key in ('source_analysis', 'how_to_play', 'mechanics', 'tags', 'fictional_reviews', 'links'):
        if not isinstance(data.get(key), list):
            raise ValueError(f'Report must have a {key} list')
    for review in data['fictional_reviews']:
        if not isinstance(review, dict) or type(review.get('rating')) is not int or not 0 <= review['rating'] <= 100:
            raise ValueError('Each fictional review rating must be an integer between 0 and 100')
    controls = data.get('controls')
    if controls is not None:
        if not isinstance(controls, dict) or set(controls) != {
                'mobile_controls', 'motion_controls', 'gamepad', 'keyboard_mouse'}:
            raise ValueError('controls must contain all four control types')
        if any(value not in ('supported', 'not_supported', 'unknown') for value in controls.values()):
            raise ValueError('Each control status must be supported, not_supported, or unknown')
    player_modes = data.get('player_modes')
    if player_modes is not None:
        if not isinstance(player_modes, dict) or set(player_modes) != {'human_players', 'modes'}:
            raise ValueError('player_modes must contain human_players and modes')
        players = player_modes['human_players']
        if players is not None and not (
                (type(players) is int and players > 0) or
                (isinstance(players, str) and players.strip())):
            raise ValueError('human_players must be a positive integer, nonempty range, or null')
        modes = player_modes['modes']
        allowed = {'single-player', 'local multiplayer', 'online multiplayer'}
        if not isinstance(modes, list) or any(not isinstance(mode, str) or mode not in allowed for mode in modes) or len(set(modes)) != len(modes):
            raise ValueError('player_modes.modes must list distinct supported modes')
    play_url = data.get('play_game_url')
    if play_url is not None and not safe_url(play_url):
        raise ValueError('play_game_url must be an HTTP(S) URL or null')
    return data


def lines_list(items):
    return [f'- {markdown(item)}' for item in items if isinstance(item, str)]


def game_readme(data):
    title = markdown(data['title'])
    url = safe_url(data['repository_url'])
    graphic = data['screenshot_based_score']
    graphic_text = 'not scored' if graphic is None else f"{graphic['score']}/100"
    out = [f'# {title}', '', f'[Open the game source]({url})' if url else 'GitHub source unavailable. Inspect the original links below.']
    if data.get('play_game_url'):
        out.append(f"[Play the game]({safe_url(data['play_game_url'])})")
    out += ['',
           f"**Overall rating:** {data['rating']['score']}/100. {markdown(data['rating'].get('reason', ''))}", '',
           f"**Screenshot score:** {graphic_text}. " +
           (markdown(graphic.get('reason', '')) if graphic else 'No inspectable gameplay screenshot.'), '']
    if data['screenshots']:
        out += ['## Screenshots', '']
        for shot in data['screenshots']:
            out += [f"![{markdown(shot.get('observation', title))}]({safe_url(shot['url'])})", '',
                    markdown(shot.get('observation', '')), '']
    for heading, key in [('Play', 'how_to_play'), ('Mechanics', 'mechanics'), ('Tags', 'tags')]:
        items = lines_list(data[key])
        if items:
            out += [f'## {heading}', '', *items, '']
    if data.get('controls') is not None:
        out += ['## Controls', '']
        labels = [('Mobile controls', 'mobile_controls'), ('Motion controls', 'motion_controls'),
                  ('Gamepad', 'gamepad'), ('Keyboard/mouse', 'keyboard_mouse')]
        statuses = {'supported': 'Supported', 'not_supported': 'Not supported',
                    'unknown': 'Not established'}
        out += [f'- {label}: {statuses[data["controls"][key]]}' for label, key in labels]
        out.append('')
    if data.get('player_modes') is not None:
        players = data['player_modes']['human_players']
        modes = data['player_modes']['modes']
        out += ['## Player modes', '',
                f'- Human players: {markdown(players) if players is not None else "Not established"}',
                f'- Modes: {markdown(", ".join(modes)) if modes else "Not established"}', '']
    if isinstance(data.get('reconstructed_prompt'), str):
        out += ['## Reconstructed prompt', '', markdown(data['reconstructed_prompt']), '']
    if data['source_analysis']:
        out += ['## Source evidence', '']
        for item in data['source_analysis']:
            if isinstance(item, dict) and safe_url(item.get('url')):
                out.append(f"- {markdown(item.get('finding', 'Evidence'))} ([source]({safe_url(item['url'])}))")
        out.append('')
    if data['fictional_reviews']:
        out += ['## Fictional reviews', '', 'Treat these as illustrative, not real user reviews.', '']
        for review in data['fictional_reviews']:
            if isinstance(review, dict):
                out.append(f"- {markdown(review.get('rating', '?'))}/100: {markdown(review.get('text', ''))}")
        out.append('')
    if data['links']:
        out += ['## Links', '']
        out += [f'- [{markdown(link)}]({safe_url(link)})' for link in data['links'] if safe_url(link)]
        out.append('')
    return '\n'.join(out).rstrip() + '\n'


def write_atomic(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + '.tmp')
    temp.write_text(content, encoding='utf-8')
    temp.replace(path)


def log(message):
    print(message, file=sys.stderr, flush=True)


def rebuild():
    entries = []
    for path in sorted(GAMES.rglob('readme.json')) if GAMES.exists() else []:
        try:
            data = validate(json.loads(path.read_text(encoding='utf-8')))
            if path.is_symlink() or any(parent.is_symlink() for parent in path.parents):
                raise ValueError('Refuse symlink report')
            write_atomic(path.with_name('README.md'), game_readme(data))
            entries.append((path.parent, data))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            log(f'Skip {path}: {exc}')
    entries.sort(key=lambda item: (-item[1]['rating']['score'], item[1]['title'].casefold(), str(item[0])))
    out = ['# Game catalog', '', 'Browse the rated games. Open each game page for evidence and play instructions.', '',
           'Add games with `./scripts/games.sh <game-url> [more-urls...]` or '
           '`./scripts/games.sh --file links.txt`. Rebuild every page and this index with '
           '`./scripts/games.sh`. Inspect `games/added.jsonl` for dated additions. '
           'Inspect `work/game-batches/` for agent logs and rejected reports.', '', '## Games', '']
    for directory, data in entries:
        target = quote(str(directory.relative_to(ROOT) / 'README.md'), safe='/')
        graphic = data['screenshot_based_score']
        graphic_text = 'not scored' if graphic is None else f"{graphic['score']}/100"
        out.append(f"- [{markdown(data['title'])}]({target}) — overall {data['rating']['score']}/100; screenshots {graphic_text}")
    if not entries:
        out.append('No valid games yet.')
    gallery = [(directory, data) for directory, data in entries
               if data['screenshot_based_score'] is not None and data['screenshots']]
    gallery.sort(key=lambda item: (-item[1]['screenshot_based_score']['score'],
                                  item[1]['title'].casefold(), str(item[0])))
    out += ['', '## Screenshot gallery', '']
    if gallery:
        out.append('<table>')
        for index in range(0, len(gallery), 3):
            row = gallery[index:index + 3]
            out.append('<tr>')
            for directory, data in row:
                shot = data['screenshots'][0]
                target = html.escape(quote(str(directory.relative_to(ROOT) / 'README.md'), safe='/'), quote=True)
                screenshot = html.escape(safe_url(shot['url']), quote=True)
                title = html.escape(data['title'], quote=True)
                observation = html.escape(str(shot.get('observation', data['title'])).replace('\n', ' '), quote=True)
                screenshot_score = data['screenshot_based_score']['score'] / 10
                out.append(
                    f'<td align="center" width="33%"><a href="{target}">'
                    f'<img src="{screenshot}" alt="{observation}" height="180"></a><br>'
                    f'<a href="{target}"><strong>{title}</strong></a> · 📸 {screenshot_score:.1f}/10</td>'
                )
            out.extend(['<td width="33%"></td>'] * (3 - len(row)))
            out.append('</tr>')
        out.extend(['</table>', ''])
    else:
        out.append('No scored screenshots yet.')
    write_atomic(ROOT / 'README.md', '\n'.join(out).rstrip() + '\n')
    print(f'Rebuilt {len(entries)} game pages and the root README.', flush=True)


def inputs(args):
    values = list(args.links)
    if args.file:
        values += [line.strip() for line in args.file.read_text(encoding='utf-8').splitlines()
                   if line.strip() and not line.lstrip().startswith('#')]
    urls = list(dict.fromkeys(input_url(value) for value in values))
    return [(url, None) for url in urls]


def analyze(items, args):
    WORK.mkdir(exist_ok=True)
    batch = WORK / 'game-batches' / (datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ') + f'-{os.getpid()}')
    batch.mkdir(parents=True)
    (batch / 'records').mkdir()
    base = test_oc.ensure_server(args, WORK)
    prompt_template = args.prompt.read_text(encoding='utf-8')
    if not prompt_template.strip():
        raise ValueError('Prompt must not be empty')
    prepared = []
    try:
        for index, (url, directory) in enumerate(items, 1):
            prompt = prompt_template.replace('{{repository_url}}', url)
            prompt = prompt.replace('{{catalog_readme_path}}', str(ROOT / 'README.md'))
            meta = test_oc.prepare(index, args, batch, base, prompt)
            prepared.append((url, directory, meta))
        def stop(*_):
            test_oc.STOP.set()
        previous = signal.signal(signal.SIGINT, stop)
        try:
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
                futures = [pool.submit(test_oc.run_one, meta, base, args.timeout)
                           for _, _, meta in prepared]
                for (url, directory, meta), future in zip(prepared, futures):
                    result = future.result()
                    item = {'url': url, 'status': 'failed', 'reason': ''}
                    try:
                        if result['status'] != 'finished':
                            raise ValueError(f"Agent {result['status']} (exit {result.get('exit_code')})")
                        report = Path(result['directory']) / 'readme.json'
                        if report.stat().st_size > 1024 * 1024:
                            raise ValueError('Report exceeds 1 MiB')
                        raw = json.loads(report.read_text(encoding='utf-8'))
                        if isinstance(raw, dict) and raw.get('rejected') in ('not_game', 'inaccessible'):
                            item.update(status=raw['rejected'], reason=str(raw.get('reason', 'No reason supplied'))[:2000])
                        else:
                            data = checked_report(raw, url)
                            item.update(status='ready', report=data)
                            if not args.defer_publish:
                                record = publish_report(data, url, {'session_id': result['session_id'],
                                    'model': args.model, 'prompt_sha256': result['prompt_sha256']})
                                item.update(status=record['status'], output=record['output'])
                                print(f"{record['status'].capitalize()} {data['title']}: {record['output']}", flush=True)
                    except (OSError, ValueError, KeyError, TypeError) as exc:
                        item.update(status='failed', reason=str(exc)[:2000])
                        log(f"Failed {url}: {exc}")
                    args.outcomes.append(item)
                    if args.summary:
                        save_summary(args)

        finally:
            signal.signal(signal.SIGINT, previous)
            test_oc.STOP.clear()
    except BaseException:
        for _, _, meta in prepared:
            result = json.loads((meta / 'result.json').read_text())
            if result['status'] in ('queued', 'running'):
                test_oc.abort(base, result)
        raise


def save_summary(args, error=None):
    write_atomic(args.summary, json.dumps({'items': args.outcomes, 'error': error}, ensure_ascii=False) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('links', nargs='*', help='Public game links, including GitHub, X, and YouTube')
    parser.add_argument('--file', type=Path, help='Read additional URLs, one per line')
    parser.add_argument('--summary', type=Path, help='Write per-input outcomes')
    parser.add_argument('--defer-publish', action='store_true', help='Return reports for a separate trusted publisher')
    parser.add_argument('--jobs', type=int, default=3, help='Maximum concurrent agents')
    parser.add_argument('--timeout', type=float, default=900, help='Seconds per agent')
    parser.add_argument('--prompt', type=Path, default=ROOT / 'prompt.md')
    parser.add_argument('--model', default=test_oc.MODEL)
    parser.add_argument('--executable', default='opencode')
    parser.add_argument('--server', help='Existing local OpenCode server URL')
    parser.add_argument('--web-base', help='Existing protected live-session URL base')
    parser.add_argument('--port', type=int, default=4096)
    args = parser.parse_args()
    args.outcomes = []
    if args.jobs < 1 or not 0 < args.timeout < float('inf'):
        parser.error('jobs and timeout must be positive and finite')
    try:
        items = inputs(args)
        WORK.mkdir(exist_ok=True)
        with (WORK / 'games.lock').open('w') as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise RuntimeError('Another game catalog run is active')
            if items:
                executable = shutil.which(args.executable)
                if not executable or not shutil.which('git'):
                    raise RuntimeError('Require opencode and git on PATH')
                args.executable = str(Path(executable).resolve())
                analyze(items, args)
            if not args.defer_publish:
                rebuild()
            if args.summary:
                save_summary(args)
        return 0
    except (OSError, ValueError, RuntimeError) as exc:
        log(str(exc))
        if args.summary:
            save_summary(args, str(exc))
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
