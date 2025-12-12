# Gnome15 Wayland Fix - Current Status

**Date**: 2025-12-12  
**Issue**: G-keys opening remote desktop connection instead of executing macros on Wayland

**Status**: ✅ FIX IMPLEMENTED - Testing Required

## Changes Made - Session 2 (2025-12-12)

### Fixed Script Macro Execution for Wayland

1. **Added `send_string_uinput()` method** (line ~457)
   - New method specifically for sending keysyms via uinput
   - Handles X11 keysym names (Super_L, Control_L, space, etc.)
   - Uses the keysym-to-uinput mapping file
   - Properly presses and releases keys

2. **Added Wayland detection to MacroHandler** (line ~151)
   - Added `is_wayland` property to MacroHandler.__init__()
   - Detects Wayland via environment variables (XDG_SESSION_TYPE, WAYLAND_DISPLAY)

3. **Modified script macro execution** (line ~647, ~654)
   - Updated `MacroScriptExecution.execute()` method
   - Added conditional logic: if Wayland, use `send_string_uinput()`, else use `send_string()`
   - Affects both `Press` and `Release` commands in script macros

4. **Added missing keysym mappings**
   - Added `Super_L=KEY_LEFTMETA` to keysym-to-uinput file
   - Added `Super_R=KEY_RIGHTMETA` to keysym-to-uinput file
   - These were needed for the language change macro (Super+Space)

### How Script Macros Work Now

- On **X11**: Uses existing methods (virtkey, XTest, or raw X11 events)
- On **Wayland**: Uses uinput for all Press/Release commands
  - Converts X11 keysym names to uinput KEY_ codes
  - Sends keys via kernel-level uinput device
  - Keys go to whatever window has focus (works correctly on Wayland)

## Changes Made - Session 1 (Previous)

### Root Cause Identified
When a G-key macro was triggered, the code was calling `get_input_focus()` to determine which window to send keys to. Under Wayland, this doesn't work correctly and was returning the wrong window (remote desktop connection window).

### Code Modifications in `src/gnome15/g15service.py`

1. **Removed X11 window focus detection** (line ~412-413)
   - No longer calls `get_input_focus()` which was causing wrong window targeting
   - Removed the X11-specific initialization code from `_do_handle()` method

2. **Created new uinput-based macro handler**
   - Added `send_simple_macro_uinput()` method (line ~331)
   - Uses kernel-level uinput system instead of X11 methods
   - Handles escape sequences (\t, \r, \n, \b, \e, \\, \p)

3. **Added character-to-uinput mapping**
   - Created `_send_char_uinput()` method (line ~381)
   - Converts characters to uinput key codes using existing keysym-to-uinput mapping file
   - Handles uppercase letters by synthesizing SHIFT+letter combinations
   - Handles special shifted characters (!, @, #, %, ^, &, *, (, ), _, +, {, }, |, :, ", <, >, ?, ~)
   - Properly presses and releases keys in correct order (press in sequence, release in reverse)

4. **Updated simple macro execution path**
   - Modified `_do_handle()` to call `send_simple_macro_uinput()` instead of `send_simple_macro()`
   - Only affects MACRO_SIMPLE type macros

### How It Works Now
- G-key presses send keystrokes via **uinput** (kernel-level input)
- Uinput sends keys as if they came from a real keyboard
- Keys go to whatever window currently has focus (works correctly on Wayland)
- No X11 dependencies for keystroke injection

## Current Status - READY FOR TESTING

### What Was Fixed
✅ Simple macros (MACRO_SIMPLE) - use uinput  
✅ Script macros (Press/Release commands) - use uinput on Wayland  
✅ Added Super_L and Super_R keysym mappings  
✅ Service is running and ready for testing

### Testing Instructions

**Test the G6 key (Language Change macro):**
1. Make sure you have a text editor or other application open
2. Press the G6 key on your keyboard
3. Expected result: Should trigger Super+Space (opens GNOME language/input source selector)

**What to look for:**
- ✅ If language selector appears: **FIX IS WORKING!**
- ❌ If nothing happens: Check logs for errors
- ❌ If remote desktop opens: X11 focus issue still present (shouldn't happen)

### If Testing Fails

Check logs for errors:
```bash
# See what happened when you pressed G6
journalctl -f | grep -i g15

# Or check the service output
tail -f /tmp/g15-start.log
```

Look for:
- "No uinput mapping found for keysym: Super_L" - means mapping didn't load
- "Unknown uinput key: KEY_LEFTMETA" - means uinput capabilities issue
- Any Python errors or exceptions

## Previous Testing Notes (Session 1)

**The Problem (Now Fixed):**
The profile uses **script** type macros with `Press`/`Release` commands. These commands were calling `send_string()` method which used X11 methods (virtkey, XTest, or raw X11 events) that don't work on Wayland.

**The Solution:**
- Created `send_string_uinput()` method for Wayland
- Added Wayland detection to MacroHandler
- Modified script execution to use uinput on Wayland
- Added missing Super_L/Super_R keysym mappings

## Technical Details

### Code Flow for Script Macros

**Before (X11 only):**
```
G-key pressed → MacroHandler._do_handle() 
→ MacroScriptExecution.execute() 
→ "press"/"release" command 
→ send_string() 
→ X11 methods (virtkey/XTest/raw events)
```

**After (Wayland-aware):**
```
G-key pressed → MacroHandler._do_handle()
→ MacroScriptExecution.execute()
→ "press"/"release" command
→ Check is_wayland
   ├─ If Wayland: send_string_uinput() → uinput
   └─ If X11: send_string() → X11 methods
```

### Key Methods

- `send_string_uinput(keysym_name, press)` - Sends X11 keysym via uinput
- `send_string(ch, press)` - Original X11 method (virtkey/XTest/raw)
- `_send_char_uinput(ch, press)` - Sends single character via uinput (for simple macros)

### Keysym to Uinput Mapping

The mapping file (`data/ukeys/keysym-to-uinput`) contains:
- Standalone keys: `space=KEY_SPACE`, `Escape=KEY_ESC`
- Modifier keys: `Control_L=KEY_LEFTCTRL`, `Super_L=KEY_LEFTMETA`
- Combinations: `Control_a=KEY_LEFTCTRL,KEY_A`

When a keysym maps to multiple keys (e.g., shifted characters), they are:
- Pressed in forward order: Shift first, then the key
- Released in reverse order: Key first, then Shift

## Files Modified in This Session

- `src/gnome15/g15service.py`
  - Added `send_string_uinput()` method (+34 lines)
  - Added `is_wayland` property to MacroHandler (+2 lines)
  - Modified Press/Release execution paths (+8 lines)
  
- `data/ukeys/keysym-to-uinput`
  - Added Super_L=KEY_LEFTMETA
  - Added Super_R=KEY_RIGHTMETA

## Files Modified Previously (Session 1)

- `src/gnome15/g15service.py` (+131 lines, -6 lines)
  - MacroHandler class: added methods for uinput-based simple macro execution
  - Removed X11 window focus dependencies

## Files to Reference

- `~/.config/gnome15/macro_profiles/g110_0/Default.macros` - current profile
- `/home/alexanderius/Projects/gnome15/data/ukeys/keysym-to-uinput` - keysym mapping file

## Useful Commands

```bash
# Start service in debug mode
cd /home/alexanderius/Projects/gnome15
./debug.sh restart

# Stop service
./debug.sh stop

# View logs (if service is running)
journalctl -f | grep g15

# Check if uinput module is loaded
lsmod | grep uinput

# Check uinput permissions
ls -la /dev/uinput
```

## References

- Script macro execution: `MacroScriptExecution.execute()` in g15service.py
- Uinput emit function: `g15uinput.emit()` in g15uinput.py
- Keysym mapping: `g15uinput.get_keysym_to_uinput_mapping()` in g15uinput.py

---

## Summary

**What was the problem?**
G-keys were opening remote desktop connections instead of executing macros on Wayland because the code was trying to get X11 window focus, which doesn't work on Wayland.

**What was fixed?**
1. **Session 1**: Simple macros now use uinput instead of X11
2. **Session 2**: Script macros (Press/Release commands) now use uinput on Wayland
3. Added Super_L and Super_R keysym mappings

**What works now?**
- ✅ Simple macros (MACRO_SIMPLE) - working with uinput
- ✅ Script macros (MACRO_SCRIPT with Press/Release) - should work with uinput
- ✅ Service starts successfully
- ⏳ **Needs testing**: Press G6 key to verify language switching works

**Next step**: Test by pressing the G6 key and see if Super+Space triggers the language selector!
