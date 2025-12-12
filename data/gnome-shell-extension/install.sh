#!/bin/bash
# Installation script for Gnome15 Window Tracker GNOME Shell Extension

set -e

EXTENSION_UUID="gnome15-window-tracker@gnome15.org"
INSTALL_DIR="$HOME/.local/share/gnome-shell/extensions/$EXTENSION_UUID"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing Gnome15 Window Tracker GNOME Shell Extension..."
echo ""

# Create installation directory
mkdir -p "$INSTALL_DIR"

# Copy extension files
echo "Copying files to $INSTALL_DIR..."
cp -v "$SCRIPT_DIR/extension.js" "$INSTALL_DIR/"
cp -v "$SCRIPT_DIR/metadata.json" "$INSTALL_DIR/"
cp -v "$SCRIPT_DIR/README.md" "$INSTALL_DIR/"

echo ""
echo "✅ Extension files installed successfully!"
echo ""
echo "Next steps:"
echo "1. Log out and log back in (required for GNOME Shell to discover the extension)"
echo "2. Enable the extension:"
echo "   gnome-extensions enable $EXTENSION_UUID"
echo "3. Verify it's working:"
echo "   gnome-extensions info $EXTENSION_UUID"
echo ""
echo "For more information, see: $INSTALL_DIR/README.md"
