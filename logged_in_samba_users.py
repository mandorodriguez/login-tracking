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

simple script I use to check if a user is connect to samba and logs the
last time seen into a python shelve. It uses a simple

smbstatus -b

command to get the logged in users.

"""

parser = argparse.ArgumentParser()
parser.add_argument("-d", "--database", type=str,
                    help="Path to an sqlite database file", required=True)
parser.add_argument("-p", "--program", type=str,
                    help="Program string to match the ps output to", default="")


args = parser.parse_args()


smbuser_output = subprocess.check_output(["smbstatus", "-d"])


curr_time = time.time()


dbfile = args.database
program_string = args.program
exclude_list = args.exclude

if args.exclude is None:
    exclude_list = []
else:
    exclude_list = args.exclude

logged_in_users = []

for l in smbuser_output.split('\n'):


    try:
        
        parts = l.split()

        if not len(parts) == 6:
            except raise Exception

        uid_num = int(parts[0])

        logged_in_users.append(parts[1])
        
    except:
        pass

pdb.set_trace()
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


