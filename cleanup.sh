#!/bin/bash

# Shopify Moose Python Demo - Cleanup Script
# Removes generated files to allow for a clean start from README instructions

set -e

echo "🧹 Shopify Moose Python Demo - Cleanup Script"
echo "=============================================="
echo

# Function to safely remove directory if it exists
remove_dir() {
    local dir="$1"
    local description="$2"
    
    if [ -d "$dir" ]; then
        echo "🗑️  Removing $description..."
        rm -rf "$dir"
        echo "   ✅ Removed: $dir"
    else
        echo "   ⚪ Not found: $dir (already clean)"
    fi
}

# Function to safely remove file if it exists
remove_file() {
    local file="$1"
    local description="$2"
    
    if [ -f "$file" ]; then
        echo "🗑️  Removing $description..."
        rm -f "$file"
        echo "   ✅ Removed: $file"
    else
        echo "   ⚪ Not found: $file (already clean)"
    fi
}

echo "Cleaning up generated files and directories..."
echo

# Remove Python virtual environment
remove_dir "venv" "Python virtual environment"

# Remove shopify connector source code folder
remove_dir "shopify" "Shopify connector source code"

# Remove Python cache directories
echo "🗑️  Removing Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
echo "   ✅ Cleaned Python cache files"

# Remove egg-info directories
remove_dir "shopify_moose_python.egg-info" "Python package metadata"

# Remove any wheel files that might have been built
echo "🗑️  Removing any wheel files..."
find . -name "*.whl" -type f -delete 2>/dev/null || true
echo "   ✅ Cleaned wheel files"

# Remove .env file for security (contains credentials)
remove_file ".env" "environment configuration file (security cleanup)"

echo
echo "🎉 Cleanup complete!"
echo
echo "📚 To start fresh, follow the README.md instructions:"
echo "   1. python3 -m venv venv"
echo "   2. source venv/bin/activate"
echo "   3. pip install -U pip wheel"
echo "   4. pip install -r requirements.txt"
echo "   5. ./setup-shopify-connector.sh"
echo "   6. cp env.example .env"
echo "   7. Edit .env with your Shopify credentials"
echo
echo "🔒 Security note: .env file was removed to prevent credential exposure"
echo
echo "Happy demo-ing! 🚀"
