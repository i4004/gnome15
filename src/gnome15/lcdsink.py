# PiTiVi , Non-linear video editor
#
#       pitivi/elements/thumbnailsink.py
#
# Copyright (c) 2005, Edward Hervey <bilboed@bilboed.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the
# Free Software Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301, USA.
"""
GdkPixbuf thumbnail sink
"""

import gi
gi.require_version('GstBase', '1.0')
from gi.repository import GstBase
gi.require_version('Gst', '1.0')
from gi.repository import GObject
from gi.repository import Gst

GObject.threads_init()
Gst.init(None)

import struct
import time

big_to_cairo_alpha_mask = struct.unpack('=i', b'\xFF\x00\x00\x00')[0]
big_to_cairo_red_mask = struct.unpack('=i', b'\x00\xFF\x00\x00')[0]
big_to_cairo_green_mask = struct.unpack('=i', b'\x00\x00\xFF\x00')[0]
big_to_cairo_blue_mask = struct.unpack('=i', b'\x00\x00\x00\xFF')[0]

class CairoSurfaceThumbnailSink(GstBase.BaseSink):
    """
    GStreamer thumbnailing sink element.

    Can be used in pipelines to generates gtk.gdk.Pixbuf automatically.
    """

    __gsignals__ = {
        "thumbnail": (GObject.SIGNAL_RUN_LAST,
                      GObject.TYPE_NONE,
                      ([GObject.TYPE_UINT64]))
        }

    __gsttemplates__ = (
        Gst.PadTemplate.new("sink",
                         Gst.PadDirection.SINK,
                         Gst.PadPresence.ALWAYS,
                         Gst.Caps.from_string("video/x-raw,"
                                  "bpp = (int) 32, depth = (int) 32,"
                                  "endianness = (int) BIG_ENDIAN,"
                                  "alpha_mask = (int) %i, "
                                  "red_mask = (int)   %i, "
                                  "green_mask = (int) %i, "
                                  "blue_mask = (int)  %i, "
                                  "width = (int) [ 1, max ], "
                                  "height = (int) [ 1, max ], "
                                  "framerate = (fraction) [ 0, 25 ]"
                                  % (big_to_cairo_alpha_mask,
                                     big_to_cairo_red_mask,
                                     big_to_cairo_green_mask,
                                     big_to_cairo_blue_mask)))
        )

    def __init__(self, *args):
        GstBase.BaseSink.__init__(self, *args)
        self.width = 1
        self.height = 1
        self.set_sync(True)
        self.data = None

    def do_set_caps(self, caps):
        self.log("caps %s" % caps.to_string())
        self.log("padcaps %s" % self.get_static_pad("sink").query_caps().to_string())
        self.width = caps.get_structure(0).get_int("width")
        self.height = caps.get_structure(0).get_int("height")
        if not caps.get_structure(0).get_name() == "video/x-raw":
            return False
        return True

    def do_render(self, buf):
        self.data = str(buf.data)
        self.emit('thumbnail', buf.timestamp)
        return Gst.FLOW_OK
 
    def do_preroll(self, buf):
        return self.do_render(buf)

GObject.type_register(CairoSurfaceThumbnailSink)
