# STATUS OF GNOME15

Gnome15 is currently **not complete maintained**.
The original primary repository has been unavailable since November 2014 due to a hosting server crash.
This fork was made to add a feature and has not been updated since November 2013, but it appears to be the latest snapshot of the repository that is currently publicly available.

I intend to bring this repository up to date with the latest version (the version before the server crash) using the code contained in the latest distribution packages available.
We want to maintain it, so many we can. Feel free to work with.

# Gnome15

A set of tools for configuring the Logitech G15 keyboard.

Contains pylibg19, a library providing support for the Logitech G19 until there
is kernel support available. It was based "Logitech-G19-Linux-Daemon" [1],
the work of "MultiCoreNop" [2].

1. http://github.com/MultiCoreNop/Logitech-G19-Linux-Daemon
2. http://github.com/MultiCoreNop

# Installation
Dependencies may be incomplete.. 

``` sh

sudo dnf install libXtst-devel libxkbfile-devel

cd ./tmp
wget https://launchpad.net/virtkey/0.63/0.63.0/+download/virtkey-0.63.0.tar.gz
tar -xf virtkey-0.63.0.tar.gz
cd virtkey-0.63.0
sudo python setup.py install
cd ../..

sudo pip install keyring

cd ./tmp
git clone https://github.com/guidugli/pyinputevent.git
cd pyinputevent
sudo python setup.py install
cd ../..

cd ./tmp
git clone https://github.com/tuomasjjrasanen/python-uinput.git
cd python-uinput
sudo python setup.py install
cd ../..

sudo autoreconf -i
sudo ./configure
make
sudo make install
```

# How to report bugs


Issues can be submited on the [github website](https://github.com/Huskynarr/gnome15/issues) [3].

3. https://github.com/Huskynarr/gnome15/issues

# Requirements

## Old
- Python 2.6
- PyUSB 0.4
- PIL (Python Image Library, just about any version should be ok)
