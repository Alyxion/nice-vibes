#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   poetry run bash scripts/run_tests_with_sample.sh [sample_name]
#
# Starts the given NiceGUI sample on http://localhost:8080 (default: dashboard),
# waits until it is reachable, then runs the full pytest suite with all opt-in
# MCP tests enabled (including screenshot tests).
#
# The sample process is stopped afterwards and port 8080 is freed, even if tests fail.
#
# This script forces NO browser popups by setting:
#   NICE_VIBES_NO_BROWSER=1

SAMPLE_NAME="${1:-dashboard}"

# Ensure nice-vibes never auto-opens a browser while running this script.
export NICE_VIBES_NO_BROWSER=1

cleanup() {
  # best-effort stop of runner
  if [[ -n "${RUNNER_PID:-}" ]] && kill -0 "$RUNNER_PID" 2>/dev/null; then
    kill -INT "$RUNNER_PID" 2>/dev/null || true
    wait "$RUNNER_PID" 2>/dev/null || true
  fi

  # ensure port is free
  poetry run nice-vibes kill-8080 >/dev/null 2>&1 || true
}
trap cleanup EXIT INT TERM

# free port up front (sample needs 8080)
poetry run nice-vibes kill-8080

# start sample runner in background (no browser popups)
poetry run nice-vibes samples run "$SAMPLE_NAME" </dev/null &
RUNNER_PID=$!

# wait for server to become reachable
echo "Waiting for http://localhost:8080 to become reachable..."
DEADLINE=$(( $(date +%s) + 45 ))
while true; do
  if curl -sf "http://localhost:8080/" >/dev/null 2>&1; then
    break
  fi
  if [[ $(date +%s) -ge $DEADLINE ]]; then
    echo "Timed out waiting for sample '$SAMPLE_NAME' to start on http://localhost:8080" >&2
    exit 1
  fi
  sleep 0.5
done

echo "Sample is up. Running full test suite (including screenshot/destructive/network tests)..."
export NICE_VIBES_RUN_DESTRUCTIVE_TESTS=1
export NICE_VIBES_RUN_NETWORK_TESTS=1
export NICE_VIBES_RUN_SCREENSHOT_TESTS=1

poetry run pytest ./tests/
