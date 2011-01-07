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

import cookielib, urllib2, urllib
from urllib2 import Request
import re

import mimetypes, mimetools

carnet_parawing_root = "http://carnet.parawing.net/"


def post_multipart(url, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        print "%s: %s" %(key, value)
        L.append(value.encode("iso-8859-1"))
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value.encode('iso-8859-1'))
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body


class ParawingException(Exception):
    pass

class Carnet:
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
        self.cookie = None
        
    def connect(self, username, password):
        data = urllib.urlencode({'login'    : username,'pass' : password})
        r = self.opener.open(carnet_parawing_root + "login.php")
#         txheaders = {'User-agent' : self.ua}

        try:

            req = Request(carnet_parawing_root + "login.php", data)
            handle = self.opener.open(req)

            for i in handle.readlines():
                m = re.search("Login ou mot de passe incorrect.", i)
                if m != None:
                    raise ParawingException("Login failed")
                        
            for index, cookie in enumerate(self.cj):
                self.cookie = "%s=%s" %(cookie.name, cookie.value)
                break # only one...!

            if self.cookie == None:
                raise LobException("No cookie found, login failed")
                        
        except IOError, e:
            print 'Error opening "%s".' % theurl
            if hasattr(e, 'code'):
                print 'Error code - %s.' % e.code
            elif hasattr(e, 'reason'):
                print "Reason :", e.reason
                print "This usually means the server doesn't exist, is down, or we don't have an internet connection."
                raise ParawingException("Error login with username [%s]" %username)


    def newFlight(self, vol):
        if self.cookie == None:
            print "You must login first"
            raise ParawingException("Login first")
        
        url = carnet_parawing_root + "insert_vol.php"
        
        form = {}

        form['jour'] = str(vol.ddate.day)
        form['mois'] = str(vol.ddate.month)
        form['annee'] = str(vol.ddate.year)

        form['site'] = "Not used"
        form['flag_site'] = '1'

        # if site_db_check enabled, then site is read from 'site_db'
        form['site_db_check'] = 'on'
        form['site_db'] = vol.deco

        form['site_atterro'] = "rrr"
        form['flag_site_atterro'] = '1'
        form['atterro_db_check'] = 'on'
        form['atterro_db'] = vol.aterro

        form['aile'] = vol.aile
        form['flag_aile'] = '1'
        # if newaile enabled, then a new wing is added
        form['newaile'] = ""

        "In minutes, max 999"
        form['duree'] = str(vol.duration.seconds / 60)

        dico = {'vol local':'40',
                'vol rando': '60',
                'cross' : '50',
                'gonflage':'1'}

        form['type'] = dico[vol.vtype]
        #one of the following:
        # Gonflage = 1
        # Pente ecole 10
        # Bi pédagogique 15
        # Plouf 20
        # Grand vol 30
        # Vol local 40
        # Cross 50
        # Triangle FAI 51
        # Triangle 52
        # Vol rando 60
        # Vol à ski 61 
        # Speed riding 62
        # Vol treuil 70
        # Pilotage 79
        # SIV 80
        # Seance wagas 90
        # Seance voltige 95
        # Competition A 96
        # Competition B 97

        # if enabled, this is a bi
        #form['biplace']

        # Takeoff time (free)
        form['heure'] = "%s:%s" % (vol.ddate.hour,vol.ddate.minute)

        form['cond_deco'] = ""
        form['cond_vol'] = ""
        form['cond_aterro'] = ""

        # in km, max 999
        form['distance'] = str(vol.dist)

        # in m, max 9999
        form['alt_max'] = str(vol.altmax)
        form['pt_bas'] = str(vol.lowestpt)

        # in m, max 9999
        form['gain_max'] = str(vol.maxgain)
        
        # in m, max 99999
        form['gain_total'] = str(vol.gaintotal)

        # free text
        form['contournement'] = ""

        # if enabled, instrument are used
        #form['instrument']

        form['cadre'] = '4'
        # one of:
        # Ecole 1
        # Club 2
        # Entre potes 3
        # Autonome 4
        
        form['stage_check'] = 'no'

        # free text, max 50chars
        form['compagnons'] = ""

        form['recit'] = vol.story

        # http link to pictures, without leading http
        form['photos'] = "marc-photos.kataplop.net"

        # upload GPS trace
        # form['file']

        form['ma_note'] = '3'
        # one of:
        # Nul 1
	# Bof 2
        # Pas mal 3
        # Top 4
        # Génial ! 5

        # if enabled, will be published
        #form['visible']

        form['choix'] = "Ajouter"

##        txheaders = {'User-agent' : self.ua, 'Cookie' : self.cookie}
		
##         req = Request(url, urllib.urlencode(form))

        print form
        
        content_type, body = encode_multipart_formdata(form.items(), {})
        headers = {'Content-Type': content_type,
                   'Content-Length': str(len(body))}
        r = urllib2.Request(url, body, headers)
#          return urllib2.urlopen(r).read()

        handle = self.opener.open(r)

        lines = handle.readlines()

        for i in lines:
            m = re.search("Vous n'êtes pas authentifié", i)
##            print i
            if m != None:
                raise ParawingException("Login timed out")
