import pymongo
import config as cfg

DB_NAME = cfg.DB_NAME

def get_db_client(conn_str: str = 'mongodb://localhost:27017/'):
    return pymongo.MongoClient(conn_str)

def get_db_info(client):
    return client.server_info()