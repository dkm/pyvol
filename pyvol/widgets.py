#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2009 Marc Poulhiès
#
# pyvol, flight logbook
#
# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Plopifier.  If not, see <http://www.gnu.org/licenses/>.

import pygtk
pygtk.require ('2.0')
import gtk.glade
import gtk.gdk
import gtk
import math

class Histogramme(gtk.DrawingArea):
    def __init__(self):
        gtk.DrawingArea.__init__(self)
        self.connect("expose_event", self.expose)


    def expose(self, widget, event):
        self.context = widget.window.cairo_create()
    
        # set a clip region for the expose event
        self.context.rectangle(event.area.x, event.area.y,
                           event.area.width, event.area.height)
        self.context.clip()
    
        self.draw(self.context)
    
        return False


    def draw_axis(self, context):
        rect = self.get_allocation()
        orig_x = rect.x + rect.width/10
        orig_y = rect.y + rect.height/10
        context.move_to(orig_x, rect.height-orig_y)

        end_x = rect.x + rect.width - rect.width/10
        end_y = rect.y + rect.height/10

        context.line_to(end_x, rect.height-end_y)
        context.stroke()

        context.move_to(orig_x, rect.height-orig_y)
        end_x = rect.x + rect.width/10
        end_y = rect.y + rect.height - rect.height/10

        context.line_to(end_x, rect.height-end_y)
        context.stroke()

        
    def draw(self, context):
        self.draw_axis(context)
