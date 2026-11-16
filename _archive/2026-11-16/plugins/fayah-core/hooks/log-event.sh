#!/usr/bin/env bash
# PostToolUse hook: record tool usage locally for the Feature Usage / DAU
# metrics described in the event-tracking skill. Reads the hook payload on
# stdin, keeps only tool name, session id and timestamp. Never blocks.
set -u
LOG_DIR="${FAYAH_HOME:-$HOME/.fayah}"
mkdir -p "$LOG_DIR" 2>/dev/null || exit 0
payload="$(cat)"
if command -v jq >/dev/null 2>&1; then
  printf '%s\n' "$payload" | jq -c \
    '{ts: (now|todate), event: "tool_used", tool: .tool_name, session: .session_id}' \
    >> "$LOG_DIR/events.jsonl" 2>/dev/null
else
  printf '{"ts":"%s","event":"tool_used","raw":true}\n' "$(date -u +%FT%TZ)" \
    >> "$LOG_DIR/events.jsonl" 2>/dev/null
fi
exit 0
