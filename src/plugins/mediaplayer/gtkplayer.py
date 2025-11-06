#!/usr/bin/python

#  Gnome15 - Suite of tools for the Logitech G series keyboards and headsets
#  Copyright (C) 2011 Brett Smith <tanktarta@blueyonder.co.uk>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.

import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk
gi.require_version('Gst', '1.0')
from gi.repository import Gst

class Main:
    def __init__(self):

        # Create GUI objects
        self.window = Gtk.Window()
        self.vbox = Gtk.VBox()
        self.da = Gtk.DrawingArea()
        self.bb = Gtk.HButtonBox()
        self.da.set_size_request(300, 150)
        self.playButton = Gtk.Button(stock="gtk - media - play")
        self.playButton.connect("clicked", self.OnPlay)
        self.stopButton = Gtk.Button(stock="gtk - media - stop")
        self.stopButton.connect("clicked", self.OnStop)
        self.quitButton = Gtk.Button(stock="gtk - quit")
        self.quitButton.connect("clicked", self.OnQuit)
        self.vbox.pack_start(self.da)
        self.bb.add(self.playButton)
        self.bb.add(self.stopButton)
        self.bb.add(self.quitButton)
        self.vbox.pack_start(self.bb)
        self.window.add(self.vbox)

        # Create GStreamer pipeline
        self.pipeline = Gst.Pipeline("mypipeline")
        # Set up our video test source
        self.videotestsrc = Gst.ElementFactory.make("videotestsrc", "video")
        # Add it to the pipeline
        self.pipeline.add(self.videotestsrc)
        # Now we need somewhere to send the video
        self.sink = Gst.ElementFactory.make("xvimagesink", "sink")
        # Add it to the pipeline
        self.pipeline.add(self.sink)
        # Link the video source to the sink - xv
        self.videotestsrc.link(self.sink)
        self.window.show_all()

    def OnPlay(self, widget):
        print("play")
        # Tell the video sink to display the output in our DrawingArea
        self.sink.set_xwindow_id(self.da.window.xid)
        self.pipeline.set_state(Gst.State.PLAYING)

    def OnStop(self, widget):
        print("stop")
        self.pipeline.set_state(Gst.State.READY)

    def OnQuit(self, widget):
        Gtk.main_quit()

start = Main()
Gtk.main() 
