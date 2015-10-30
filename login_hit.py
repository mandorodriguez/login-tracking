import os
import pwd
import pdb
import argparse
import time
import shelve
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



if not user_id in exclude_list:

    #
    # caution, will add a '.db' to the file name
    # 
    shv = shelve.open(dbfile, writeback=True)

    
    if shv.has_key(user_id):

        login_list = shv[user_id]['logins']
    
        login_list.append(curr_time)

        shv[user_id]['logins'] = login_list

        shv[user_id]['last'] = curr_time

    else:
        shv[user_id] = {'logins': [curr_time] , 'last' : curr_time}



    shv.close()


