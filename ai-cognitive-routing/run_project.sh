#!/usr/bin/env bash
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PARENT_DIR="$(dirname "$PROJECT_DIR")"
PROJECT_VENV="$PROJECT_DIR/venv"
PARENT_VENV="$PARENT_DIR/venv"
PYTHON_BIN=""

pick_python_from_venv() {
  local venv_dir="$1"

  if [[ -x "$venv_dir/bin/python3" ]]; then
    PYTHON_BIN="$venv_dir/bin/python3"
    return 0
  fi

  if [[ -x "$venv_dir/bin/python" ]]; then
    PYTHON_BIN="$venv_dir/bin/python"
    return 0
  fi

  return 1
}

ensure_python_bin() {
  # Prefer project-local venv for portability; fall back to parent-level venv.
  if pick_python_from_venv "$PROJECT_VENV"; then
    return
  fi

  if pick_python_from_venv "$PARENT_VENV"; then
    return
  fi

  echo "No virtual environment found. Creating one in $PROJECT_VENV"
  python3 -m venv "$PROJECT_VENV"

  if ! pick_python_from_venv "$PROJECT_VENV"; then
    echo "Error: failed to locate Python in $PROJECT_VENV after creation." >&2
    exit 1
  fi
}

ensure_dependencies() {
  if ! "$PYTHON_BIN" -c "import langgraph" >/dev/null 2>&1; then
    echo "Installing dependencies from requirements.txt ..."
    "$PYTHON_BIN" -m pip install -r "$PROJECT_DIR/requirements.txt"
  fi
}

main() {
  ensure_python_bin
  ensure_dependencies

  echo "Running AI Cognitive Routing project ..."
  "$PYTHON_BIN" "$PROJECT_DIR/main.py"
}

main
