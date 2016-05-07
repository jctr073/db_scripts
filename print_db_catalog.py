#!/usr/local/bin/python
# -*- coding: utf-8 -*-

# This script will print out a complete list of tables 
# definitions for the database specified.
# Required arguments: host, port, user, password, database

import MySQLdb as mdb
import sys

def pad_str(val, pad):
    if val is None:
        val = 'NULL'
    return val.ljust(pad)

host = sys.argv[1] 
port = int(sys.argv[2])
usr  = sys.argv[3] 
pwd  = sys.argv[4]
db   = sys.argv[5]

# Open connection
con = mdb.connect(host=host, port=port, user=usr, passwd=pwd, db=db)

with con:

    # Get a list of tables from information schema
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = '%s'" % db
    cur = con.cursor(mdb.cursors.DictCursor)
    cur.execute(sql)
    tables = cur.fetchall()

    # Process each table
    for tbl in tables:

        # Get table column descriptions
        sql = "DESC %s " % tbl['TABLE_NAME']
        cur = con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print "\n" + tbl['TABLE_NAME']

        # Setup and print column headers
        desc = cur.description
        print "-" * 27, "-" * 22, "-" * 4, "-" * 3, "-" * 17, "-" * 26
        print "{}                       {}                   {} {} {}           {}" \
            .format(desc[0][0], desc[1][0], desc[2][0], desc[3][0], desc[4][0], desc[5][0])
        print "-" * 27, "-" * 22, "-" * 4, "-" * 3, "-" * 17, "-" * 26

        # Print padding row values
        for row in rows:
            print "{}{}{}{}{}{}".format(row[0].ljust(28), row[1].ljust(23), row[2].ljust(5), 
                row[3].ljust(4), pad_str(row[4], 18), row[5].ljust(27))



