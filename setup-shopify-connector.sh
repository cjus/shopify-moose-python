#!/bin/bash
set -euo pipefail

# Install connector repo
REPO_BRANCH=carlos/shopify-python-connector bash -i <(curl -fsSL https://connectors.514.ai/install.sh) shopify v2025-07 514-labs python

cd shopify/data-api

# Ensure build tools are installed
pip install --upgrade pip build

# Build distributions (wheel + sdist) into ./dist/
python -m build

# Find latest built wheel and install it
WHEEL_PATH=$(ls -t dist/*.whl | head -n 1 || true)
if [[ -z "${WHEEL_PATH:-}" ]]; then
  echo "ERROR: No wheel found in $(pwd)/dist. Build may have failed." >&2
  exit 1
fi
echo "Installing connector wheel: ${WHEEL_PATH}"
pip install "${WHEEL_PATH}"

cd ..
