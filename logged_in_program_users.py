#!/usr/bin/env python
import os
import pwd
import pdb
import argparse
import time
import shelve
import psutil
import subprocess
"""

simple script I use to check if a process is running for a user. In this
case just looking to see who is mounting the samba daemon but you can
stick anything in the -p arg. Nothing fancy.

"""

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", type=str,
                    help="Path to an sqlite database file", required=True)
parser.add_argument("-p", "--program", type=str,
                    help="Program string to match the ps output to", default="")
parser.add_argument("-x", "--exclude", type=str, 
                    nargs='*', help="List of users to exclude")

args = parser.parse_args()


grep_output = subprocess.check_output(["ps", "aux"])


curr_time = time.time()


dbfile = args.database
program_string = args.program
exclude_list = args.exclude

if args.exclude is None:
    exclude_list = []
else:
    exclude_list = args.exclude

logged_in_users = []

for l in grep_output.split('\n'):

    if program_string in l:

        try:
            user_id = l.split()[0]

            if not user_id in logged_in_users and not user_id in exclude_list and not user_id.isdigit():
                logged_in_users.append(user_id)
        except:
            pass

#
# caution, will add a '.db' to the file name
#
shv = shelve.open(dbfile, protocol=1, writeback=True)

# loop through all users and log the last time they were logged in
for user_id in logged_in_users:
    
    if not user_id in exclude_list:
        
        if shv.has_key(user_id):

            #shv[user_id]['prev'] = shv[user_id]['last']
            
            shv[user_id]['last'] = curr_time

        else:
            #shv[user_id] = {'last' : curr_time, 'prev' : curr_time}
            shv[user_id] = {'last' : curr_time}

shv.close()


