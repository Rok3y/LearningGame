import pymongo
import config as cfg
from logging_config import logger

DB_NAME = cfg.DB_NAME
DB_CONNECTION_STRING = cfg.DB_CONNECTION_STRING

# def get_db_client(conn_str: str = 'mongodb://localhost:27017/'):
#     return pymongo.MongoClient(conn_str)

# def get_db_info(client):
#     return client.server_info()

class MongoDBClient:
    _client = None
    def __init__(self) -> None:
        pass

    @classmethod
    def get_client(cls):
        if cls._client is None:
            try:
                cls._client = pymongo.MongoClient(DB_CONNECTION_STRING)
                logger.debug("MongoDB client created")
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {e}")
                cls._client = None  # Reset client on failure
        return cls._client