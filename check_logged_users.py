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

user_list = []

for key,value in shv.iteritems():

    user_list.append( (key, int(time.time())-int(value['last'])) )
    #datetime.datetime.fromtimestamp(value['last'])
    


# now print them after sorting

print "\nUsername\tTime since last login:"

for u in sorted(user_list, key=lambda tup: tup[1]):
    print "%s\t\t%s" % (u[0], datetime.timedelta(seconds=u[1]))

print "\n"

shv.close()


