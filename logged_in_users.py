#!/usr/bin/env python
import os
import pwd
import pdb
import argparse
import time
import shelve
import psutil
"""

This script is just used to log the user that executes it into
a database to collect login data. I can exclude users and via a list on the
command line.

"""

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", type=str,
                    help="Path to an sqlite database file", required=True)
parser.add_argument("-x", "--exclude", type=str, 
                    nargs='*', help="List of users to exclude")

args = parser.parse_args()


user_id = pwd.getpwuid( os.getuid() ).pw_name
curr_time = time.time()


dbfile = args.database

if args.exclude is None:
    exclude_list = []
else:
    exclude_list = args.exclude



logged_in_users = list(set([u.name for u in psutil.get_users()]))

#
# caution, will add a '.db' to the file name
#
shv = shelve.open(dbfile, protocol=1, writeback=True)

# loop through all users and log the last time they were logged in
for user_id in logged_in_users:
    
    if not user_id in exclude_list:
        
        if shv.has_key(user_id):

            shv[user_id]['prev'] = shv[user_id]['last']
            
            shv[user_id]['last'] = curr_time

        else:
            shv[user_id] = {'last' : curr_time, 'prev' : curr_time}

shv.close()


