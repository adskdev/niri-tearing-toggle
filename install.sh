#!/usr/bin/env bash
set -e

INSTALL_DIR="$HOME/.local/bin"
SCRIPT_NAME="niri-tearing-toggle"
SOURCE_FILE="toggle-tearing.py"

echo "Installing Niri Tearing Toggle..."

mkdir -p "$INSTALL_DIR"

cp "$SOURCE_FILE" "$INSTALL_DIR/$SCRIPT_NAME"
chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

echo "=========================================="
echo "Installation complete!"
echo "The script is installed at: $INSTALL_DIR/$SCRIPT_NAME"
echo ""
echo "Make sure '$INSTALL_DIR' is in your system's PATH."
echo ""
echo "Next step: Add a keybind to your Niri config!"
echo "Check the README.md for configuration examples."
echo "=========================================="