#!/usr/bin/env bash
set -euo pipefail

SESSION="cat_rmi"
MAIN_WIN="stack"

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
NS_LOG="/tmp/${SESSION}_ns.log"
SERVER_LOG="/tmp/${SESSION}_server.log"

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux not found. Install tmux first."
  exit 1
fi

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "Session '$SESSION' already exists."
  echo "Use: tmux attach -t $SESSION"
  exit 1
fi

rm -f "$NS_LOG" "$SERVER_LOG"

# Cria 1 janela com 3 panes: cliente (topo), server (baixo esq), nameserver (baixo dir)
tmux new-session -d -s "$SESSION" -n "$MAIN_WIN" "cd '$ROOT_DIR' && bash"
tmux split-window -v -t "$SESSION:$MAIN_WIN.0" -l 33% "cd '$ROOT_DIR' && bash"
tmux split-window -h -t "$SESSION:$MAIN_WIN.1" -l 50% "cd '$ROOT_DIR' && bash"
tmux select-layout -t "$SESSION:$MAIN_WIN" main-horizontal

CLIENT_PANE="$SESSION:$MAIN_WIN.0"
SERVER_PANE="$SESSION:$MAIN_WIN.1"
NS_PANE="$SESSION:$MAIN_WIN.2"

# 1) Sobe Name Server
tmux send-keys -t "$NS_PANE" "cd '$ROOT_DIR' && uv run python -u -m Pyro5.nameserver --host 127.0.0.1 2>&1 | tee '$NS_LOG'" C-m

echo "Waiting Name Server to be ready..."
for _ in {1..30}; do
  if grep -Eq "NS running on|Pyro\.NameServer" "$NS_LOG" 2>/dev/null; then
    break
  fi
  sleep 1
done

if ! grep -Eq "NS running on|Pyro\.NameServer" "$NS_LOG" 2>/dev/null; then
  echo "Name Server did not start successfully."
  echo "Check logs in tmux session '$SESSION'."
  exit 1
fi

# 2) Sobe servidor apenas após NS pronto
tmux send-keys -t "$SERVER_PANE" "cd '$ROOT_DIR' && uv run python -u cat_server.py 2>&1 | tee '$SERVER_LOG'" C-m

echo "Waiting RMI server to register in Name Server..."
for _ in {1..30}; do
  if grep -q "Registered in Name Server as: reinaldoKN" "$SERVER_LOG" 2>/dev/null; then
    break
  fi
  sleep 1
done

if ! grep -q "Registered in Name Server as: reinaldoKN" "$SERVER_LOG" 2>/dev/null; then
  echo "RMI server did not register successfully."
  echo "Check logs in tmux session '$SESSION'."
  exit 1
fi

# 3) Sobe cliente apenas após servidor registrar
tmux send-keys -t "$CLIENT_PANE" "cd '$ROOT_DIR' && uv run python cat_client.py" C-m

tmux select-pane -t "$CLIENT_PANE"
echo "Session '$SESSION' started with 1 window and 3 panes (client top, server+nameserver bottom)."
echo "Attach with: tmux attach -t $SESSION"
