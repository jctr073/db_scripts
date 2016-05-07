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

# Open connection
con = mdb.connect(host=sys.argv[1], port=int(sys.argv[2]), 
    user=sys.argv[3], passwd=sys.argv[4], db=sys.argv[5])

with con:

    # Get a list of tables from information schema
    sql = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'iqter'"
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
        print "{Field}                       {Type}                   {Null} {Key} {Default}           {Extra}" \
        .format(Field=desc[0][0], Type=desc[1][0], Null=desc[2][0], 
            Key=desc[3][0], Default=desc[4][0], Extra=desc[5][0])
        print "-" * 27, "-" * 22, "-" * 4, "-" * 3, "-" * 17, "-" * 26

        # Print padding row values
        for row in rows:
            print "{}{}{}{}{}{}".format(row[0].ljust(28), row[1].ljust(23), row[2].ljust(5), 
                row[3].ljust(4), pad_str(row[4], 18), row[5].ljust(27))
            # print row


