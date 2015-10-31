#!/usr/bin/env python
import os
import pwd
import pdb
import argparse
import datetime
import shelve
import time

"""

Just loops through the previous database generated on login hits and prints the
time since last login.

"""

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", type=str,
                    help="Path to an sqlite database file", required=True)


args = parser.parse_args()




dbfile = args.database



shv = shelve.open(dbfile, protocol=1)

print ""
for key,value in shv.iteritems():

    #datetime.datetime.fromtimestamp(value['last'])
    
    print "%s\tTime since last login\t%s" % (key, datetime.timedelta(seconds=int(time.time())-int(value['last'])) )


print "\n"

shv.close()


