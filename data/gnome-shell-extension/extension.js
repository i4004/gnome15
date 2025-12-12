import Gio from 'gi://Gio';
import GLib from 'gi://GLib';
import GObject from 'gi://GObject';
import Shell from 'gi://Shell';
import Meta from 'gi://Meta';

const DBUS_INTERFACE = `
<node>
  <interface name="org.gnome15.WindowTracker">
    <method name="GetActiveWindow">
      <arg type="s" direction="out" name="wm_class"/>
      <arg type="s" direction="out" name="title"/>
    </method>
    <signal name="ActiveWindowChanged">
      <arg type="s" name="wm_class"/>
      <arg type="s" name="title"/>
    </signal>
  </interface>
</node>`;

const WindowTrackerDBus = GObject.registerClass(
class WindowTrackerDBus extends GObject.Object {
    constructor() {
        super();
        this._dbusImpl = Gio.DBusExportedObject.wrapJSObject(DBUS_INTERFACE, this);
    }

    GetActiveWindow() {
        try {
            const display = global.display;
            const focusWindow = display.focus_window;
            
            if (focusWindow) {
                const wmClass = focusWindow.get_wm_class() || '';
                const title = focusWindow.get_title() || '';
                return [wmClass, title];
            }
        } catch (e) {
            console.error('Error getting active window:', e);
        }
        return ['', ''];
    }

    export(connection, path) {
        this._dbusImpl.export(connection, path);
    }

    unexport() {
        this._dbusImpl.unexport();
    }

    emitActiveWindowChanged(wmClass, title) {
        this._dbusImpl.emit_signal('ActiveWindowChanged',
            GLib.Variant.new('(ss)', [wmClass, title]));
    }
});

export default class Extension {
    constructor() {
        this._dbus = null;
        this._ownerId = 0;
        this._focusWindowId = 0;
        this._lastWmClass = '';
        this._lastTitle = '';
    }

    enable() {
        console.log('Enabling Gnome15 Window Tracker extension');
        
        // Create D-Bus service
        this._dbus = new WindowTrackerDBus();
        
        // Own the bus name
        this._ownerId = Gio.bus_own_name(
            Gio.BusType.SESSION,
            'org.gnome15.WindowTracker',
            Gio.BusNameOwnerFlags.NONE,
            (connection) => {
                // Bus acquired
                console.log('D-Bus name acquired');
                this._dbus.export(connection, '/org/gnome15/WindowTracker');
            },
            () => {
                // Name acquired
                console.log('D-Bus name org.gnome15.WindowTracker acquired');
            },
            () => {
                // Name lost
                console.error('Could not acquire D-Bus name org.gnome15.WindowTracker');
            }
        );

        // Monitor focus window changes
        const display = global.display;
        this._focusWindowId = display.connect('notify::focus-window', () => {
            this._onFocusWindowChanged();
        });

        // Emit initial state
        this._onFocusWindowChanged();
    }

    disable() {
        console.log('Disabling Gnome15 Window Tracker extension');
        
        // Disconnect signals
        if (this._focusWindowId) {
            global.display.disconnect(this._focusWindowId);
            this._focusWindowId = 0;
        }

        // Unexport D-Bus object
        if (this._dbus) {
            this._dbus.unexport();
            this._dbus = null;
        }

        // Release bus name
        if (this._ownerId) {
            Gio.bus_unown_name(this._ownerId);
            this._ownerId = 0;
        }

        this._lastWmClass = '';
        this._lastTitle = '';
    }

    _onFocusWindowChanged() {
        try {
            const display = global.display;
            const focusWindow = display.focus_window;

            if (focusWindow) {
                const wmClass = focusWindow.get_wm_class() || '';
                const title = focusWindow.get_title() || '';

                // Only emit if changed
                if (wmClass !== this._lastWmClass || title !== this._lastTitle) {
                    this._lastWmClass = wmClass;
                    this._lastTitle = title;
                    
                    console.log(`Active window changed: ${wmClass} - ${title}`);
                    
                    if (this._dbus) {
                        this._dbus.emitActiveWindowChanged(wmClass, title);
                    }
                }
            }
        } catch (e) {
            console.error('Error in _onFocusWindowChanged:', e);
        }
    }
}
