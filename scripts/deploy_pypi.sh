#!/bin/bash
# Deploy the package to PyPI
#
# Usage:
#   ./scripts/deploy_pypi.sh [--test]
#
# Options:
#   --test    Deploy to TestPyPI instead of production PyPI
#
# Prerequisites:
#   - Built wheel in dist/ (run ./scripts/build.sh first)
#   - poetry-plugin-pypi-token or PYPI_TOKEN environment variable
#   - For TestPyPI: TEST_PYPI_TOKEN environment variable
#
# Recommended workflow:
#   ./scripts/build.sh        # Build the wheel
#   ./scripts/test_wheel.sh   # Test it locally
#   ./scripts/deploy_pypi.sh  # Deploy to PyPI

set -e

cd "$(dirname "$0")/.."

# Check that dist/ exists and has files
if [ ! -d "dist" ] || [ -z "$(ls -A dist 2>/dev/null)" ]; then
    echo "Error: No built package found in dist/"
    echo "Run ./scripts/build.sh first"
    exit 1
fi

echo "=== Package to deploy ==="
ls -la dist/
echo ""

# Check for --test flag
USE_TEST_PYPI=false
if [[ "$1" == "--test" ]]; then
    USE_TEST_PYPI=true
fi

if $USE_TEST_PYPI; then
    echo "=== Deploying to TestPyPI ==="
    poetry config repositories.testpypi https://test.pypi.org/legacy/
    poetry publish -r testpypi
    echo ""
    echo "=== Deployed to TestPyPI ==="
    echo "Install with: pip install -i https://test.pypi.org/simple/ nice-vibes"
else
    echo "=== Deploying to PyPI ==="
    poetry publish
    echo ""
    echo "=== Deployed to PyPI ==="
    echo "Install with: pip install nice-vibes"
fi
