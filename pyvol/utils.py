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

from datetime import timedelta

def convert_time_to_tdelta(sqltime):
    # SQL time should be hh:mm:ss
    hh,mm,ss = sqltime.split(':')
    return timedelta(hours=int(hh), minutes=int(mm), seconds=int(ss))

def convert_tdelta_to_minutes(tdelta):
    hh,mm,ss = str(tdelta).split(':')
    minutes = int(hh)*60+int(mm)
    if int(ss)>59:
        minutes += int(ss)/60

    return minutes
