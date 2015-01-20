#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, sys, cairo, gobject
from math import pi
import time, threading

class sleep_and_die(threading.Thread):
    def run(self):
        time.sleep(5)
        gtk.main_quit()

def expose (widget, event):
    cr = widget.window.cairo_create()

    # Sets the operator to clear which deletes everything below where an object is drawn
    cr.set_operator(cairo.OPERATOR_CLEAR)
    # Makes the mask fill the entire window
    cr.rectangle(0.0, 0.0, *widget.get_size())
    # Deletes everything in the window (since the compositing operator is clear and mask fills the entire window
    cr.fill()
    # Set the compositing operator back to the default
    cr.set_operator(cairo.OPERATOR_OVER)

    # Load image
    image = cairo.ImageSurface.create_from_png("./bullshit.png")
    cr.set_source_surface(image, 0, 0)
    cr.paint()

gobject.threads_init()

win = gtk.Window()
win.connect("destroy", lambda q: gtk.main_quit())
win.set_decorated(False)
win.set_position(gtk.WIN_POS_MOUSE)
win.set_skip_taskbar_hint(True)
win.set_size_request(450, 205)
win.set_keep_above(True)

# Makes the window paintable, so we can draw directly on it
win.set_app_paintable(True)

# This sets the windows colormap, so it supports transparency.
# This will only work if the wm support alpha channel
screen = win.get_screen()
rgba = screen.get_rgba_colormap()
win.set_colormap(rgba)

win.connect('expose-event', expose)
win.show()

t = sleep_and_die()
t.start()
gtk.main()

