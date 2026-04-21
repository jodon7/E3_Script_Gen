#!/usr/bin/env bash
set -e

echo "Cleaning previous builds..."
rm -rf build dist D2E.spec

echo "Building D2E executable..."
pyinstaller --clean \
  --onefile \
  --noconsole \
  --name D2E \
  --icon Designer.ico \
  --add-data "fdc_template.txt:." \
  gui.py

echo "Build complete!"
echo "Output located at: dist/D2E.exe"
