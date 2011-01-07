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

from utils import convert_tdelta_to_minutes
from pylab import *
from sqlite import DateFilter

def get_flight_durations(db, start=None, end=None):
    
    if start != None or end != None:
        df = DateFilter(dateGt=start, dateLt=end)
    else:
        df = None
        
    fls = db.getVols(sfilter=df)
    dur = [convert_tdelta_to_minutes(fl.duration) for fl in fls]

    f = [fl.ddate for fl in fls]

    dates = date2num(f)

    return dur,dates

