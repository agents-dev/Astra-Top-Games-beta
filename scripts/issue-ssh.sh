#!/usr/bin/env bash
set -euo pipefail
ssh_dir="${RUNNER_TEMP}/issue-ssh"
mkdir -p "$ssh_dir" "$HOME/.ssh"
chmod 700 "$ssh_dir" "$HOME/.ssh"
test -n "$AGENTSWEB_SSH_PUBLIC_KEY"
printf '%s\n' "$AGENTSWEB_SSH_PUBLIC_KEY" > "$HOME/.ssh/authorized_keys"
chmod 600 "$HOME/.ssh/authorized_keys"
sudo apt-get update -qq
sudo apt-get install -y -qq openssh-server
sudo mkdir -p /run/sshd
sudo /usr/sbin/sshd -D -e -p 2222 -o PasswordAuthentication=no -o PermitRootLogin=no -o PubkeyAuthentication=yes > "$ssh_dir/sshd.log" 2>&1 &
git clone --depth 1 --filter=blob:none --sparse https://github.com/agents-dev/agent-workspace.git "$ssh_dir/client"
git -C "$ssh_dir/client" sparse-checkout set lolgames_tunnel
name="catalog-${GITHUB_RUN_ID}-${GITHUB_RUN_ATTEMPT}-ssh"
port=$((32000 + GITHUB_RUN_ID % 1000))
nohup env PYTHONPATH="$ssh_dir/client" python3 -m lolgames_tunnel client 127.0.0.1:2222 \
  --server agentsweb.space --name "$name" --public-port "$port" > "$ssh_dir/tunnel.log" 2>&1 < /dev/null &
echo $! > "$ssh_dir/tunnel.pid"
for _ in {1..60}; do
  grep -q '^ssh://' "$ssh_dir/tunnel.log" && break
  kill -0 "$(cat "$ssh_dir/tunnel.pid")"
  sleep 1
done
endpoint="$(sed -nE 's#^ssh://([^:[:space:]]+):([0-9]+).*$#\1 \2#p' "$ssh_dir/tunnel.log" | head -n 1)"
read -r host port <<< "$endpoint"
test -n "$host" && test -n "$port"
command="ssh -tt -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -i ~/.ssh/aiplay-agentsweb -p $port runner@$host"
printf '%s\n' "$command"
{ printf '## SSH debug worker\n\n```sh\n%s\n```\n' "$command"; } >> "$GITHUB_STEP_SUMMARY"
