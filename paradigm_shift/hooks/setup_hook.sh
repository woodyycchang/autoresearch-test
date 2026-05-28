#!/usr/bin/env bash
# setup_hook.sh — install the Run 13 pre-tool hook on the user's machine.
#
# Idempotent: safe to re-run. Backs up any existing settings.json/hook copy
# before writing a new one.
#
# Usage:
#   ./paradigm_shift/hooks/setup_hook.sh           # install into ~/.claude
#   CLAUDE_HOME=/custom/path ./setup_hook.sh       # install elsewhere
#
# Emergency disable:
#   mv ~/.claude/settings.json ~/.claude/settings.json.disabled

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
CLAUDE_HOME="${CLAUDE_HOME:-$HOME/.claude}"
HOOKS_SRC="${REPO_ROOT}/paradigm_shift/hooks/pre_tool.py"
POST_SRC="${REPO_ROOT}/paradigm_shift/hooks/post_tool.py"
HOOKS_DEST_DIR="${CLAUDE_HOME}/hooks"
HOOKS_DEST="${HOOKS_DEST_DIR}/pre_tool.py"
POST_DEST="${HOOKS_DEST_DIR}/post_tool.py"
SETTINGS_DEST="${CLAUDE_HOME}/settings.json"
BACKUP_TS="$(date +%Y%m%dT%H%M%S)"

echo "[setup_hook] repo root: ${REPO_ROOT}"
echo "[setup_hook] target:    ${CLAUDE_HOME}"

for src in "${HOOKS_SRC}" "${POST_SRC}"; do
  if [ ! -f "${src}" ]; then
    echo "[setup_hook] ERROR: ${src} not found" >&2
    exit 1
  fi
done

mkdir -p "${HOOKS_DEST_DIR}"

# 1. Install the hooks (back up the old ones if they differ)
install_hook() {
  local src="$1" dest="$2"
  if [ -f "${dest}" ] && ! diff -q "${src}" "${dest}" >/dev/null 2>&1; then
    cp "${dest}" "${dest}.bak.${BACKUP_TS}"
    echo "[setup_hook] backed up existing hook to ${dest}.bak.${BACKUP_TS}"
  fi
  cp "${src}" "${dest}"
  chmod 0755 "${dest}"
  echo "[setup_hook] installed ${dest}"
}
install_hook "${HOOKS_SRC}" "${HOOKS_DEST}"   # PreToolUse  enforcement
install_hook "${POST_SRC}"  "${POST_DEST}"    # PostToolUse + Stop [REPORT] injection

# 2. Wire it into ~/.claude/settings.json (back up first)
if [ -f "${SETTINGS_DEST}" ]; then
  cp "${SETTINGS_DEST}" "${SETTINGS_DEST}.bak.${BACKUP_TS}"
  echo "[setup_hook] backed up existing settings to ${SETTINGS_DEST}.bak.${BACKUP_TS}"
fi

cat > "${SETTINGS_DEST}" <<JSON
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "python3 ${HOOKS_DEST}" }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "*",
        "hooks": [
          { "type": "command", "command": "python3 ${POST_DEST}" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python3 ${POST_DEST}" }
        ]
      }
    ]
  }
}
JSON
chmod 0644 "${SETTINGS_DEST}"
echo "[setup_hook] wrote ${SETTINGS_DEST}"

# 3. Generate per-session HMAC key (rotate only if missing)
REPO_CLAUDE_DIR="${REPO_ROOT}/.claude"
KEY_PATH="${REPO_CLAUDE_DIR}/.checkpoint-key"
mkdir -p "${REPO_CLAUDE_DIR}"
if [ ! -f "${KEY_PATH}" ]; then
  python3 -c "import secrets,sys; sys.stdout.buffer.write(secrets.token_bytes(32))" > "${KEY_PATH}"
  chmod 0400 "${KEY_PATH}"
  echo "[setup_hook] generated per-session HMAC key at ${KEY_PATH} (mode 0400)"
else
  echo "[setup_hook] HMAC key already exists at ${KEY_PATH} (leave intact)"
fi

echo
echo "[setup_hook] done."
echo
echo "Verify the hook allows itself:"
echo "  /bin/sh -c \"python3 ${HOOKS_DEST}\" && echo OK"
echo
echo "Run the test suite:"
echo "  python3 ${REPO_ROOT}/paradigm_shift/hooks/test_pre_tool.py"
echo
echo "Emergency disable:"
echo "  mv ${SETTINGS_DEST} ${SETTINGS_DEST}.disabled"
