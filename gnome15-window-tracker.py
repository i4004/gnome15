#!/usr/bin/env python3
"""
Gnome15 Window Tracker - Monitors active window on Wayland
Writes active window information to ~/.cache/gnome15/active_window
"""

import os
import time
import subprocess
import signal
import sys

STATE_FILE = os.path.expanduser("~/.cache/gnome15/active_window")
CHECK_INTERVAL = 0.5  # Check every 500ms

def get_active_window():
    """Try to get active window using various methods"""
    
    # Method 1: Try GNOME Shell via busctl
    try:
        result = subprocess.run(
            ['busctl', '--user', 'call', 'org.gnome.Shell',
             '/org/gnome/Shell', 'org.gnome.Shell', 'Eval', 's',
             'global.display.focus_window ? global.display.focus_window.get_wm_class() + "|" + global.display.focus_window.get_title() : ""'],
            capture_output=True, text=True, timeout=1
        )
        if result.returncode == 0 and 'bs true' in result.stdout:
            # Extract the window info from output
            lines = result.stdout.split('\n')
            for line in lines:
                if '|' in line:
                    # Extract from quotes
                    start = line.find('"')
                    end = line.rfind('"')
                    if start >= 0 and end > start:
                        info = line[start+1:end]
                        if '|' in info:
                            parts = info.split('|', 1)
                            return (parts[0], parts[1])
    except Exception:
        pass
    
    # Method 2: Try getting from /proc (find process with most recent window focus)
    # This is a fallback and may not be accurate
    try:
        # Get currently focused process (best effort)
        result = subprocess.run(['pgrep', '-n', '-x', 'firefox|chrome|chromium|code|gedit|nautilus'],
                              capture_output=True, text=True)
        if result.returncode == 0:
            pid = result.stdout.strip()
            # Read process name
            with open(f'/proc/{pid}/comm', 'r') as f:
                name = f.read().strip()
                return (name, name)
    except Exception:
        pass
    
    return None

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    print("\nStopping window tracker...")
    sys.exit(0)

def main():
    # Ensure cache directory exists
    cache_dir = os.path.dirname(STATE_FILE)
    os.makedirs(cache_dir, exist_ok=True)
    
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("Gnome15 Window Tracker started")
    print(f"Writing to: {STATE_FILE}")
    print("Press Ctrl+C to stop\n")
    
    last_window = None
    
    while True:
        try:
            window = get_active_window()
            
            if window and window != last_window:
                wm_class, title = window
                print(f"Active window: {wm_class} - {title}")
                
                # Write to state file
                with open(STATE_FILE, 'w') as f:
                    f.write(f"{wm_class}\n{title}\n")
                
                last_window = window
            
            time.sleep(CHECK_INTERVAL)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == '__main__':
    main()
