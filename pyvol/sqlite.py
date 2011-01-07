from pysqlite2 import dbapi2 as sqlite
from pyvol.common import Vol,Aile
from datetime import timedelta,date,datetime

from utils import *

class DateFilter:
    def __init__(self, dateGt=None, dateLt=None, columnName='ddate'):
        self.gt = dateGt
        self.lt = dateLt
        self.colname = columnName
        
    def __str__(self):
        strrep = ""
        
        if self.gt != None:
            strrep += " %s >= '%s'" %(self.colname, self.gt)

        if self.lt != None:
            if strrep != "":
                strrep += " AND "
            strrep += " %s <= '%s'" %(self.colname, self.lt)

        return strrep

class PySqlite:
    def __init__(self, filename):
        self.con = sqlite.connect(filename)
        self.cur = self.con.cursor()
        self.con.row_factory = sqlite.Row
        
    def save(self, persitable):
        sql = persitable.persistme()
        print sql
        self.cur.execute(sql)
        self.con.commit()        
        
    def get(self, table, sfilter=None):
        sql = "SELECT * FROM %s" %table
        if sfilter != None:
            sql += " WHERE %s" %sfilter

        self.cur.execute(sql)

        return self.cur.fetchall()

    def getVols(self, sfilter=None):
        sql = "SELECT * FROM vols" 

        if sfilter != None:
            sql += " WHERE %s" %sfilter

        sql += " ORDER BY ddate"

        print sql
        self.cur.execute(sql)

        indexes = [f[0] for f in self.cur.description]
        vols=[]
        fieldIndices = range(len(self.cur.description))
        
        for avol in self.cur.fetchall():
            vold={}
            for i in fieldIndices:
                vold[indexes[i]]=avol[i]

            dur = convert_time_to_tdelta(vold['duration'])
            
            y,m,d = map(int,vold['ddate'].split()[0].split('-'))

            hour,min,sec = map(int,vold['ddate'].split()[1].split(':'))
            
            ddate = datetime(y,m,d,hour,min,sec)
            
            vols.append(Vol(ddate,
                            dur,
                            vold['dist'],
                            vold['altmax'],
                            vold['maxgain'],
                            vold['gaintotal'],
                            vold['lowestpt'],
                            vold['aile'],
                            vold['deco'],
                            vold['aterro'],
                            vold['story'],
                            vold['vtype'],
                            vold['id']))
        return vols

    def getWings(self, sfilter=None):
        sql = "SELECT * FROM ailes"

        if sfilter != None:
            sql += " WHERE %s" %sfilter

        sql += " ORDER BY iname"

        self.cur.execute(sql)
        
        indexes = [f[0] for f in self.cur.description]
        wings=[]
        fieldIndices = range(len(self.cur.description))
        
        for awing in self.cur.fetchall():
            wingd={}
            for i in fieldIndices:
                wingd[indexes[i]]=awing[i]
            wings.append(Aile(wingd['iname'],
                              wingd['infos']))
        return wings

    def getLocation(self, tablename, sfilter=None):
        sql = "SELECT * FROM %s" %tablename

        if sfilter != None:
            sql += " WHERE %s" %sfilter

        sql += " ORDER BY iname"
        self.cur.execute(sql)
        
        indexes = [f[0] for f in self.cur.description]
        ls=[]
        fieldIndices = range(len(self.cur.description))
        
        for al in self.cur.fetchall():
            ld={}
            for i in fieldIndices:
                ld[indexes[i]]=al[i]
            ls.append(Aile(ld['iname'],
                            ld['infos']))
        return ls
        
    def getTakeoff(self, sfilter=None):
        return self.getLocation("decos", sfilter)

    def getLanding(self, sfilter=None):
        return self.getLocation("aterros", sfilter)

    def byebye(self):
        self.cur.close()
        self.con.close()
