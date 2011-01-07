from datetime import timedelta

from utils import *

class PyVolException(Exception):
    pass

class Persist:
    def persistme(self):
        attrs = [x for x in dir(self) if x.startswith("_p_")]
        sql_attrs = [x[3:] for x in dir(self) if x.startswith("_p_")]
        sql = "INSERT INTO %s (%s) " %(self.pclass, ", ".join(sql_attrs))
        sql += " VALUES (%s)" %", ".join(["'%s'"%str(self.__dict__[x]) for x in attrs])

        return sql

    def __getattr__(self, name):
        return self.__dict__["_p_%s" %name]

class Vol(Persist):
    def __init__(self, ddate, duration,
                 dist, altmax, maxgain, gaintotal,
                 lowestpt, aile, deco, aterro, story, vtype,
                 idd=None):
        
        self.pclass = "vols"
        self._p_ddate = ddate

        # converts a duration string into a timedelta object
        if timedelta(days=1) <= duration:
            raise PyVolException()
        
        self._p_duration = duration
##        self._p_hdeco = hdeco
        self._p_dist = dist
        self._p_altmax = altmax
        self._p_maxgain = maxgain
        self._p_gaintotal = gaintotal
        self._p_lowestpt = lowestpt
        self._p_aile = aile
        self._p_deco = deco
        self._p_aterro = aterro
        self._p_story = story.replace("'", "''")
        self._p_vtype = vtype
        # if this object is linked to a database row, this is its
        # unique ID!
        self.id = idd

##    def __cmp__(self, other):
        # compare 2 flight wrt. the takeoff date/

class Location(Persist):
    def __init__(self, iname, infos):
        self._p_iname = iname
        self._p_infos = infos

    def __str__(self):
        return "iname[%s], infos[%s]" %(self._p_iname, self._p_infos)
        
class Deco(Location):
    def __init__(self, iname, infos):
        self.pclass = "decos"
        Location.__init__(self, iname,infos)
        

class Aterro(Location):
    def __init__(self, iname, infos):
        self.pclass = "aterros"
        Location.__init__(self, iname,infos)

class Aile(Persist):
    def __init__(self, iname, infos):
        self.pclass = "ailes"
        self._p_iname = iname
        self._p_infos = infos

