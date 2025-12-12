# Installing Gnome15 Window Tracker Extension

## Quick Installation

1. **Navigate to the extension directory** (or copy just the `data/gnome-shell-extension` folder)

2. **Run the installation script:**
   ```bash
   cd /path/to/gnome15/data/gnome-shell-extension
   ./install.sh
   ```

3. **Log out and log back in** (required for GNOME Shell to discover the extension)

4. **Enable the extension:**
   ```bash
   gnome-extensions enable gnome15-window-tracker@gnome15.org
   ```

5. **Verify it's working (optional):**
   ```bash
   # Check if extension is enabled
   gnome-extensions list --enabled | grep gnome15
   
   # Test the D-Bus service
   busctl --user call org.gnome15.WindowTracker \
       /org/gnome15/WindowTracker \
       org.gnome15.WindowTracker \
       GetActiveWindow
   ```

## What This Extension Does

- Tracks the currently active window on Wayland
- Provides window information to Gnome15 via D-Bus
- Enables automatic macro profile switching based on active application
- Works with GNOME Shell 45-50

## Files Included

- `extension.js` - Main extension code (154 lines)
- `metadata.json` - Extension metadata
- `README.md` - Detailed documentation
- `install.sh` - Automatic installation script
- `INSTALL.md` - Installation guide

## Troubleshooting

**Extension not appearing after installation?**
- You MUST log out and log back in for GNOME Shell to discover it

**Extension won't enable?**
- Check GNOME Shell version compatibility (45-50 supported)
- Check logs: `journalctl -f /usr/bin/gnome-shell`

**D-Bus service not working?**
- Extension must be enabled first
- Try: `gnome-extensions info gnome15-window-tracker@gnome15.org`

## Integration with Gnome15

Once installed and enabled, the Gnome15 service will automatically:
1. Connect to the extension's D-Bus service
2. Listen for window change events
3. Switch macro profiles based on active application

No additional configuration needed!
