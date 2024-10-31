import pymongo
import config as cfg
from src.logging_config import logger

DB_NAME = cfg.DB_NAME
DB_CONNECTION_STRING = cfg.DB_CONNECTION_STRING

TICKER_COLLECTION = 'tickers'
COMPANY_COLLECTION = 'companies'

# def get_db_client(conn_str: str = 'mongodb://localhost:27017/'):
#     return pymongo.MongoClient(conn_str)

# def get_db_info(client):
#     return client.server_info()

class MongoDBManager:
    _client = None
    _db = None
    _comapny_collection = None
    _ticker_collection = None
    
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
    
    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls._db = cls.get_client()[DB_NAME]
        return cls._db
    
    @classmethod
    def get_company_collection(cls):
        if cls._comapny_collection is None:
            cls._comapny_collection = cls.get_db()[COMPANY_COLLECTION]
        return cls._comapny_collection
    
    @classmethod
    def get_ticker_collection(cls):
        if cls._ticker_collection is None:
            cls._ticker_collection = cls.get_db()[TICKER_COLLECTION]
        return cls._ticker_collection