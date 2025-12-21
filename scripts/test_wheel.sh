#!/bin/bash
# Test the built wheel before deployment
#
# Usage:
#   ./scripts/test_wheel.sh
#
# This script:
#   1. Creates a temporary virtual environment
#   2. Installs the built wheel
#   3. Runs basic smoke tests
#   4. Cleans up

set -e

cd "$(dirname "$0")/.."

# Check that dist/ exists and has a wheel
WHEEL=$(ls dist/*.whl 2>/dev/null | head -1)
if [ -z "$WHEEL" ]; then
    echo "Error: No wheel found in dist/"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

echo "=== Testing wheel: $WHEEL ==="
echo ""

# Create temp directory for test venv
TMPDIR=$(mktemp -d)
trap "rm -rf $TMPDIR" EXIT

echo "=== Creating test virtual environment ==="
poetry run python3 -m venv "$TMPDIR/venv"
source "$TMPDIR/venv/bin/activate"

echo "=== Installing wheel ==="
pip install "$WHEEL"

echo "=== Running smoke tests ==="
echo ""

# Test 1: CLI help
echo "Test 1: nice-vibes --help"
nice-vibes --help > /dev/null
echo "  ✓ CLI runs"

# Test 2: List samples
echo "Test 2: nice-vibes list"
nice-vibes list > /dev/null
echo "  ✓ Samples list works"

# Test 3: MCP config
echo "Test 3: nice-vibes mcp-config"
nice-vibes mcp-config > /dev/null
echo "  ✓ MCP config works"

# Test 4: Import package
echo "Test 4: Import nice_vibes"
python -c "import nice_vibes; print(f'  ✓ Package imports (version in wheel)')"

echo ""
echo "=== All tests passed ==="
echo ""
echo "Wheel is ready for deployment: $WHEEL"
