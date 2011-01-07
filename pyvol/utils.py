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
