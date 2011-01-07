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
