#!/usr/bin/env bash
set -euo pipefail

# Resolve the directory this script lives in (even if symlinked)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Paths
VENV_PYTHON="$SCRIPT_DIR/.venv/bin/python"
PYTHON_SCRIPT="$SCRIPT_DIR/py_mos_docx_parser.py"
LOG_FILE="$SCRIPT_DIR/cron.log"

# Move into the project directory
cd "$SCRIPT_DIR"

# Run the script
"$VENV_PYTHON" "$PYTHON_SCRIPT" >> "$LOG_FILE" 2>&1

current_date=$(date +"%Y-%m-%d")

echo "🔐 Adding SSH key..."
export GPG_TTY=$(tty)
eval "$(ssh-agent -s)"
ssh-add /home/beloved/.ssh/github || { echo "❌ Failed to add SSH key"; exit 1; }
git push