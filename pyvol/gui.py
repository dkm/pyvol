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

import os

interface_file='../glade/pyvol/pyvol.glade'

from common import *
from sqlite import PySqlite

from utils import convert_tdelta_to_minutes

from datetime import date,time,timedelta,datetime

from pyvol.parawing import Carnet


USER="marcus"
PASSWORD=XXXXXX

sqlite = PySqlite("test")

class NewWing:
    def __init__(self, callback=None):
        self.filename = os.path.join(os.path.dirname(__file__), interface_file)

        self.xml = gtk.glade.XML(self.filename, root="new_wing_window")
        self.xml.signal_autoconnect(self)  

        self.rootwin = self.xml.get_widget("new_wing_window")
        
        self.rootwin.set_title("Add a new wing")

        # do we need to notify someone for these changes ?
        self.callback = callback
#        self.rootwin.show_all()
                
    def destroy(self):
        if self.callback != None:
            self.callback()
        
        self.rootwin.destroy()

    def on_cancel_button_clicked(self, widget):
        self.destroy()

    def on_add_button_clicked(self, widget):
        wingname = self.xml.get_widget("wingname_entry").get_text()
        infos = self.xml.get_widget("infos_entry").get_text()
        f = Aile(wingname, infos)
        sqlite.save(f)
        self.destroy()

class NewLocation:
    def __init__(self, theclass, title, callback=None):
        self.filename = os.path.join(os.path.dirname(__file__), interface_file)

        self.xml = gtk.glade.XML(self.filename, root="new_location_window")
        self.xml.signal_autoconnect(self)  

        self.rootwin = self.xml.get_widget("new_location_window")
        self.new_class = theclass
        
        self.rootwin.set_title("Add a new %s" %title)

        # do we need to notify someone for these changes ?
        self.callback = callback
        
    def destroy(self):
        if self.callback != None:
            self.callback()
        
        self.rootwin.destroy()

    def on_cancel_button_clicked(self, widget):
        self.destroy()

    def on_add_button_clicked(self, widget):
        location = self.xml.get_widget("location_entry").get_text()
        infos = self.xml.get_widget("infos_entry").get_text()
        f = self.new_class(location, infos)
        sqlite.save(f)
        self.destroy()

class NewVol:

    def createCombo(self, widgetname):
        """Creates comboxes from string list
        """
        combobox = self.xml.get_widget(widgetname)

        liststore =  gtk.ListStore(str)
        combobox.set_model(liststore)
            
        cell = gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text',0)



    def updateCombo(self, widgetname, strlist):
        cb = self.xml.get_widget(widgetname)
        liststore = cb.get_model()

        liststore.clear()
        
        for i in strlist:
            liststore.append([i])

        if cb.get_active() == -1:
            cb.set_active(0)
        

    def updateWingCombo(self):
        self.updateCombo("wing_combobox",
                         [f.iname for f in sqlite.getWings()])

    def updateTakeoffCombo(self):
        self.updateCombo("takeoff_location_combobox",
                         [f.iname for f in sqlite.getTakeoff()])

    def updateLandingCombo(self):
        self.updateCombo("landing_location_combobox",
                         [f.iname for f in sqlite.getLanding()])
    
    def __init__(self):
        """Creates a new window for creating a new flight
        """
	self.filename = os.path.join(os.path.dirname(__file__), interface_file)

        self.xml = gtk.glade.XML(self.filename, root="new_vol_window")
        self.xml.signal_autoconnect(self)  
        self.rootwin = self.xml.get_widget("new_vol_window")

        self.createCombo("wing_combobox")
        self.updateWingCombo()
        
        self.createCombo("takeoff_location_combobox")
        self.updateTakeoffCombo()
        
        self.createCombo("landing_location_combobox"),

        self.updateLandingCombo()

        self.createCombo("flight_type_combobox")
        self.updateCombo("flight_type_combobox", ["vol local", "vol rando", "cross", "gonflage"])
        
    def destroy(self):
        self.rootwin.destroy()

    def on_new_takeoff_button_clicked(self, widget):
        NewLocation(Deco, "Takeoff", self.updateTakeoffCombo)
    
    def on_new_landing_button_clicked(self, widget):
        NewLocation(Aterro, "Landing", self.updateLandingCombo)

    def on_new_wing_button_clicked(self, widget):
        NewWing(self.updateWingCombo)

    def on_cancel_button_clicked(self, widget):
        self.destroy()
    
    def on_save_button_clicked(self, widget):
        d_tuple = self.xml.get_widget("date_calendar").get_date()
        # month + 1 because month is 0 based (strange... but it's how gtk works...)

        dhours = self.xml.get_widget("hours_duration_spinbutton").get_value()
        dmins = self.xml.get_widget("mins_duration_spinbutton").get_value()
        duration = timedelta(hours=dhours, minutes=dmins)

        tot_h = self.xml.get_widget("takeoff_time_hour_spinbutton").get_value()
        tot_m = self.xml.get_widget("takeoff_time_mins_spinbutton").get_value()
        
        ddate = datetime(d_tuple[0], d_tuple[1]+1, d_tuple[2], tot_h, tot_m)
        
        dist = self.xml.get_widget("distance_spinbutton").get_value()
        altmax = self.xml.get_widget("altmax_spinbutton").get_value()
        maxgain = self.xml.get_widget("maxgain_spinbutton").get_value()
        gaintotal = self.xml.get_widget("total_gain_spinbutton").get_value()
        lowestpt = self.xml.get_widget("altlow_spinbutton").get_value()
        aile = self.xml.get_widget("wing_combobox").get_active_text()
        deco = self.xml.get_widget("takeoff_location_combobox").get_active_text()
        aterro = self.xml.get_widget("landing_location_combobox").get_active_text()

        vtype = self.xml.get_widget("flight_type_combobox").get_active_text()
        
        story_buffer = self.xml.get_widget("story_textview").get_buffer()
        story = story_buffer.get_text(story_buffer.get_start_iter(),
                                      story_buffer.get_end_iter())

        v = Vol(ddate, duration, dist,
                altmax, maxgain, gaintotal,
                lowestpt, aile, deco, aterro, story, vtype)
        
        sqlite.save(v)

        self.destroy()


class DisplayFlight:
    def __init__(self, vol):
	self.filename = os.path.join(os.path.dirname(__file__), interface_file)
        self.xml = gtk.glade.XML(self.filename, root="display_flight_window")
        self.xml.signal_autoconnect(self)

        self.xml.get_widget("date_label").set_text(str(vol.ddate.date()))
        self.xml.get_widget("duration_label").set_text(str(vol.duration))
        
        self.xml.get_widget("takeoff_time_label").set_text(str(vol.ddate.time()))
        self.xml.get_widget("takeoff_location_label").set_text(vol.deco)
        self.xml.get_widget("landing_location_label").set_text(vol.aterro)
        self.xml.get_widget("distance_label").set_text(str(vol.dist))
        self.xml.get_widget("altmax_label").set_text(str(vol.altmax))
        self.xml.get_widget("altlow_label").set_text(str(vol.lowestpt))
        self.xml.get_widget("maxgain_label").set_text(str(vol.maxgain))
        self.xml.get_widget("total_gain_label").set_text(str(vol.gaintotal))
        self.xml.get_widget("wing_label").set_text(vol.aile)
        self.xml.get_widget("flight_type_label").set_text(str(vol.vtype))

        self.vol = vol

        tb = gtk.TextBuffer()
        tb.set_text(vol.story)
        
        self.xml.get_widget("story_textview").set_buffer(tb)

    def on_upload_pw_button_clicked(self, widget):
        c = Carnet()
        c.connect(USER, PASSWORD)
        c.newFlight(self.vol)
        
    def on_close_button_clicked(self, widget):
        self.xml.get_widget("display_flight_window").destroy()
        

class BrowseVols:
    def __init__(self):
	self.filename = os.path.join(os.path.dirname(__file__), interface_file)
        self.xml = gtk.glade.XML(self.filename, root="browse_window")
        self.xml.signal_autoconnect(self)
	self.treestore = None

        self.current_vol = None

        self.treeview = self.xml.get_widget("vols_treeview")
        self.build_treeview()
        
        self.refresh_treeview()


    def on_vols_treeview_row_activated(self, path, column, user_data):
        DisplayFlight(self.current_vol)

    def on_vols_treeview_cursor_changed(self, user_data):
        path,focus = self.treeview.get_cursor()
        itera = self.treeview.get_model().get_iter(path)
        
        self.current_vol = self.treestore.get_value(itera, 4)
        
    
    def on_close_button_clicked(self, widget):
        win = self.xml.get_widget("browse_window")
        win.destroy()
        
    def add_col(self, treeview, name, num):
        col = gtk.TreeViewColumn(name)
        treeview.append_column(col)
        cell = gtk.CellRendererText()
        col.pack_start(cell, True)
        col.add_attribute(cell, 'text', num)
        treeview.set_search_column(num)
        col.set_sort_column_id(num)

    def build_treeview(self):
        self.treestore = gtk.TreeStore(str, str, str, int, object)
        
        self.treeview.set_model(self.treestore)

        self.add_col(self.treeview, "Date", 0)
        self.add_col(self.treeview, "Deco", 1)
        self.add_col(self.treeview, "Duree", 2)
        self.add_col(self.treeview, "Km", 3)

        self.treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)

    def refresh_treeview(self):
        self.treestore.clear()

        vols = sqlite.getVols()
        for vol in vols:
            self.treestore.append(None, (vol.ddate.date(), vol.deco, vol.duration, vol.dist, vol))
            
##        self.treestore.append(None, ("19 dec 07", "St Hilaire", 3, 50))
			
    def upload_row(self, treemodel, path, iter):
        vol = self.treestore.get_value(iter, 4)
        c = Carnet()
        c.connect(USER, PASSWORD)
        c.newFlight(vol)


    def on_upload_pw_button_clicked(self, widget):
        self.treeview.get_selection().selected_foreach(self.upload_row)

class GUI:
	def __init__(self):
		self.filename = os.path.join(os.path.dirname(__file__), interface_file)
		self.xml = gtk.glade.XML(self.filename, root="pyvol_window")
                
		# autoconnect signals to this class' methods
		self.xml.signal_autoconnect(self)

                gtk.main()

        def on_browsevols_button_clicked(self, widget):
            BrowseVols()

        def on_new_vol_button_clicked(self, widget):
            NewVol()

        def on_close_button_clicked(self, widget):
            gtk.main_quit()
