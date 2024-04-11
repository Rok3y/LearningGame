import pymongo
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def get_db_client(conn_str: str = 'mongodb://localhost:27017/'):
    return pymongo.MongoClient(conn_str)

def get_db_info(client):
    return client.server_info()