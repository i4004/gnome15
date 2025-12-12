#!/bin/bash
# Test script for Gnome15 Window Tracker extension

echo "Gnome15 Window Tracker Extension Test"
echo "======================================"
echo

# Check if extension is installed
if [ -d "$HOME/.local/share/gnome-shell/extensions/gnome15-window-tracker@gnome15.org" ]; then
    echo "✓ Extension is installed"
else
    echo "✗ Extension is NOT installed"
    exit 1
fi

# Check if extension is enabled
if gnome-extensions list --enabled 2>/dev/null | grep -q "gnome15-window-tracker@gnome15.org"; then
    echo "✓ Extension is enabled"
else
    echo "⚠ Extension is NOT enabled"
    echo "  Trying to enable..."
    gnome-extensions enable gnome15-window-tracker@gnome15.org 2>&1
    if [ $? -eq 0 ]; then
        echo "  ✓ Extension enabled successfully"
    else
        echo "  ✗ Failed to enable extension"
        echo "  You may need to log out and log back in, then run:"
        echo "  gnome-extensions enable gnome15-window-tracker@gnome15.org"
        exit 1
    fi
fi

echo
echo "Testing D-Bus service..."
echo

# Test if D-Bus service is available
if busctl --user tree org.gnome15.WindowTracker >/dev/null 2>&1; then
    echo "✓ D-Bus service is running"
    
    # Test GetActiveWindow method
    echo "  Testing GetActiveWindow method..."
    result=$(busctl --user call org.gnome15.WindowTracker /org/gnome15/WindowTracker org.gnome15.WindowTracker GetActiveWindow 2>&1)
    if [ $? -eq 0 ]; then
        echo "  ✓ GetActiveWindow works!"
        echo "  Result: $result"
    else
        echo "  ✗ GetActiveWindow failed: $result"
    fi
    
    # Monitor for window changes
    echo
    echo "Monitoring for window changes (switch windows to test)..."
    echo "Press Ctrl+C to stop"
    echo
    busctl --user monitor org.gnome15.WindowTracker --match="type='signal',interface='org.gnome15.WindowTracker'"
    
else
    echo "✗ D-Bus service is NOT running"
    echo
    echo "This means the extension is not loaded yet."
    echo
    echo "Please follow these steps:"
    echo "1. Log out and log back in"
    echo "2. Run this test script again"
    echo
    echo "OR check the extension logs:"
    echo "  journalctl -f /usr/bin/gnome-shell"
fi
