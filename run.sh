#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🛠️ Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "▶️ Starting The Codebase: Legacy of the Root..."
python3 main.py