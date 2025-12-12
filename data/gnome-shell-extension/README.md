# Gnome15 Window Tracker Extension

This GNOME Shell extension provides active window tracking for Gnome15 on Wayland.

## What it does

- Tracks the currently active window (WM_CLASS and title)
- Exposes this information via D-Bus
- Sends signals when the active window changes
- Allows Gnome15 to automatically switch macro profiles based on active application

## Installation

### Automatic Installation

From the gnome15 repository:

```bash
cd ~/Projects/gnome15/data/gnome-shell-extension
./install.sh
```

### Manual Installation

```bash
INSTALL_DIR="$HOME/.local/share/gnome-shell/extensions/gnome15-window-tracker@gnome15.org"
mkdir -p "$INSTALL_DIR"
cp extension.js metadata.json README.md "$INSTALL_DIR/"
```

## Activation

**IMPORTANT**: On Wayland, GNOME Shell needs to be restarted to discover new extensions.

### Steps:

1. **Log out and log back in** (simplest method)

2. **After logging back in**, enable the extension:
   ```bash
   gnome-extensions enable gnome15-window-tracker@gnome15.org
   ```

3. **Verify it's working**:
   ```bash
   cd ~/Projects/gnome15
   ./test-window-tracker-extension.sh
   ```

## Testing

Run the test script to check if everything is working:

```bash
cd ~/Projects/gnome15
./test-window-tracker-extension.sh
```

The script will:
- Check if the extension is installed
- Check if it's enabled  
- Test the D-Bus service
- Monitor for window changes

## D-Bus Interface

**Service Name**: `org.gnome15.WindowTracker`  
**Object Path**: `/org/gnome15/WindowTracker`  
**Interface**: `org.gnome15.WindowTracker`

### Methods

- `GetActiveWindow() → (wm_class: string, title: string)`
  - Returns the WM_CLASS and title of the currently focused window

### Signals

- `ActiveWindowChanged(wm_class: string, title: string)`
  - Emitted when the active window changes

## Manual Testing

```bash
# Check if service is running
busctl --user tree org.gnome15.WindowTracker

# Get current active window
busctl --user call org.gnome15.WindowTracker /org/gnome15/WindowTracker org.gnome15.WindowTracker GetActiveWindow

# Monitor window changes (switch windows to see updates)
busctl --user monitor org.gnome15.WindowTracker
```

## Troubleshooting

### Extension not showing up

```bash
# List all extensions
gnome-extensions list | grep gnome15

# If not listed, you need to log out and log back in
```

### Extension won't enable

```bash
# Check extension status
gnome-extensions info gnome15-window-tracker@gnome15.org

# Check GNOME Shell logs for errors
journalctl -f /usr/bin/gnome-shell
```

### D-Bus service not available

The extension must be enabled and GNOME Shell must be restarted (via logout/login) for the D-Bus service to become available.

## Integration with Gnome15

Once the extension is enabled, the Gnome15 service will automatically:
1. Try to connect to the D-Bus service
2. Listen for window change signals
3. Automatically switch macro profiles based on active application

No additional configuration needed - it just works!

## Files

- `extension.js` - Main extension code
- `metadata.json` - Extension metadata
