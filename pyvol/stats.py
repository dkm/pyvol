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

