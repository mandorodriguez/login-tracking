#!/usr/bin/env python
import os
import pwd
import pdb
import argparse
import datetime
import shelve
import psutil
"""

Just loops through the previous database generated on login hits and prints their
most recent login and the one before that.


"""

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", type=str,
                    help="Path to an sqlite database file", required=True)


args = parser.parse_args()




dbfile = args.database



shv = shelve.open(dbfile, protocol=1)

print ""
for key,value in shv.iteritems():

    print "%s: last login %s, previous %s" % (key, datetime.datetime.fromtimestamp(value['last']), datetime.datetime.fromtimestamp(value['prev']))


print "\n"

shv.close()


