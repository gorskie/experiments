
"""
This module contains the functions that will be used to query the mongoDB

Dependencies:
    pymongo
"""
from pymongo import MongoClient


def connect_mongo_db(host_name, port_number):
    # Todo: move hostname into .env
    if host_name is None:
        host_name = 'localhost'
    if port_number is None:
        port_number = '27017'
    client = MongoClient(host_name, port_number)
    try:
        print(client.server_info())

    except Exception:
        print("Unable to connect to the server.")

    return client


# def load_db_from_disk(client, db_name):
#     """ 
#     loads data from disk. 
#     do NOT commit that data to the repo! 

#     to find 'data_loc' do the following:
#     1.  connect to mongo via terminal and use any db
#     2.  type db.serverCmdLineOpts()
#     3.  look for the value stored in the "parsed/storage/dbPath" attributes.
#         ex. "dbPath" : "/usr/local/var/mongodb" (this path should be correct for homebrew users)
#     4. move the data to this path
#     """

    


def get_done_counts(client, db_name):
    dockets_count = int(client[db_name]['dockets'].count_documents({}))
    docs_count = int(client[db_name]['documents'].count_documents({}))
    comments_count = int(client[db_name]['comments'].count_documents({}))
    return dockets_count + docs_count + comments_count



client = connect_mongo_db()
print(get_done_counts(client, "mirrulations"))
