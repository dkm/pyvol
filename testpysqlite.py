#!/usr/bin/env python

from pysqlite2 import dbapi2 as sqlite

con = sqlite.connect("test") 

# Get a Cursor object that operates in the context of Connection con:
cur = con.cursor()

# Execute the SELECT statement:
cur.execute("SELECT * FROM vols")

# Retrieve all rows as a sequence and print that sequence:
print cur.fetchall()
