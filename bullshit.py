#!/usr/bin/env python

import pygtk
pygtk.require('2.0')

import gtk
import os
import sys
import cairo
import gobject
import time
import threading
import argparse


image = cairo.ImageSurface.create_from_png('./images/bullshit.png')


class sleep_and_die(threading.Thread):
    def __init__(self, time):
        self.time = time
        super(sleep_and_die, self).__init__()

    def run(self):
        time.sleep(self.time)
        gtk.main_quit()


def expose(widget, event):
    global image

    cr = widget.window.cairo_create()

    # Sets the operator to clear which deletes everything below where
    # an object is drawn
    cr.set_operator(cairo.OPERATOR_CLEAR)
    # Makes the mask fill the entire window
    cr.rectangle(0.0, 0.0, *widget.get_size())
    # Deletes everything in the window (since the compositing operator
    # is clear and mask fills the entire window
    cr.fill()
    # Set the compositing operator back to the default
    cr.set_operator(cairo.OPERATOR_OVER)

    # Load image
    cr.set_source_surface(image, 0, 0)
    cr.paint()


def main():
    global image

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--image', type=str, required=False)
    parser.add_argument('-t', '--time', type=int, default=5, required=False)
    args = parser.parse_args()

    if args.image is not None:
        try:
            image = cairo.ImageSurface.create_from_png(
                os.path.expanduser(args.image))
        except cairo.Error:
            sys.stderr.write('file "%s" not found\n' % args.image)
            sys.exit(2)

    gobject.threads_init()

    win = gtk.Window()
    win.connect("destroy", lambda q: gtk.main_quit())
    win.set_decorated(False)
    win.set_position(gtk.WIN_POS_MOUSE)
    win.set_skip_taskbar_hint(True)
    win.set_size_request(image.get_width(), image.get_height())
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

    t = sleep_and_die(args.time)
    t.start()
    gtk.main()

if __name__ == "__main__":
    main()
