# After update python

## in gnome15

* Download and install https://launchpad.net/virtkey/
* (sudo?) pip install python-uinput
* pip install pyalsaaudio
* Change python version to required in configure.ac
* autoreconf -f -i -Wall,no-obsolete
* ./configure
* sudo make
* sudo make install
* copy gnome15 module from old installation to new (from /usr/lib/python3.11/site-packages/gnome15 to /usr/local/lib/python3.11/site-packages/gnome15)
* start g15-desktop-service