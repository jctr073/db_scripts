#!/usr/bin/python
# -*- coding: utf-8 -*-

# At the time of this writing, RDS doesn't allow access to
# slave_skip_errors, so this script polls slave status and 
# calls the mysql.rds_skip_repl_error stored procedure.
# Required arguments: host, port, user, password, database

import MySQLdb as mdb
import time
import sys

con = mdb.connect(host=sys.argv[1], port=int(sys.argv[2]), 
    user=sys.argv[3], passwd=sys.argv[4], db=sys.argv[5])

SHORT_INTERVAL = 3
LONG_INTERVAL  = 60

with con:

    print '====================== RDS Replication Monitor ======================'

    # continuos loop
    while (True):

        repeat = True

        # check for slave errors
        while (repeat):
            cur = con.cursor(mdb.cursors.DictCursor)
            cur.execute('SHOW SLAVE STATUS')
            row = cur.fetchone()

            if row['Last_SQL_Errno']:

                # Log the error and call skip procedure
                print 'err desc: ', row['Last_SQL_Error']
                cur2 = con.cursor()
                cur2.execute('CALL mysql.rds_skip_repl_error')

                # Replication errors can come in waves, so check for more errors
                time.sleep(SHORT_INTERVAL)
            else:
                # log some stats and skip repeat
                print time.strftime("%c"), ' > Behind: ', row['Seconds_Behind_Master'], ' Pos: ', row['Exec_Master_Log_Pos'], ' Slave_SQL_Running'
                repeat = False

        # Sleep before checking again
        time.sleep(LONG_INTERVAL)

print "done!"