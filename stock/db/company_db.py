import scrape as sc
import pandas as pd
from logging_config import logger
import db.db_common as dbc
import pymongo
#logger = logging.getLogger('StocksLogger')

COMPANY_COLLECTION = 'companies'
BULK_SIZE = 100
operations = []

def get_company_document(ticker: str):
    logger.debug(f'Get company document ({ticker}) from database.')
    client = dbc.MongoDBClient.get_client()
    db = client[dbc.DB_NAME]
    collection = db[COMPANY_COLLECTION]
    
    try:
        collection = collection.find_one({'ticker': ticker})
        if collection is None:
            logger.warning(f'Company document ({ticker}) not found in database.')
    except Exception as e:
        logger.error(f'Error getting company document ({ticker}) from database.')
        logger.error(e)
    
    return collection

def add_company_document(document: dict):
    ticker = document["ticker"]
    logger.debug(f'Storing company document ({ticker}) in database.')
    try:
        client = dbc.MongoDBClient.get_client()
        db = client[dbc.DB_NAME]
        collection = db[COMPANY_COLLECTION]
        
        collection.insert_one(document)
    except Exception as e:
        logger.error(f'Error storing company document ({ticker}) in database.')
        logger.error(e)
    
    logger.debug(f'Company document ({ticker}) stored in database.')

def update_company_document(document: dict):
    ticker = document["ticker"]
    logger.debug(f'Updating company document ({ticker}) in database.')
    try:
        client = dbc.MongoDBClient.get_client()
        db = client[dbc.DB_NAME]
        collection = db[COMPANY_COLLECTION]
        
        collection.update_one({'ticker': ticker}, {'$set': document})
    except Exception as e:
        logger.error(f'Error updating company document ({ticker}) in database.')
        logger.error(e)
    
    logger.debug(f'Company document ({ticker}) updated in database.')
    
def add_or_update_company_document(document: dict):
    ticker = document["ticker"]
    logger.debug(f'Storing company document ({ticker}) in database.')
    try:
        client = dbc.MongoDBClient.get_client()
        db = client[dbc.DB_NAME]
        collection = db[COMPANY_COLLECTION]
        
        result = collection.update_one(
            {'ticker': ticker},
            {'$set': document},
            upsert=True
        )
    except Exception as e:
        logger.error(f'Error storing company document ({ticker}) in database.')
        logger.error(e)
        return None
    
    logger.debug(f'Company document ({ticker}) stored in database.')
    return result

def add_or_update_company_document_bulk(document: dict):
    ticker = document["ticker"]
    
    op = pymongo.UpdateOne(
        {'ticker': ticker},
        {'$set': document},
        upsert=True
    )
    operations.append(op)
    
    if len(operations) >= BULK_SIZE:
        try:
            client = dbc.MongoDBClient.get_client()
            db = client[dbc.DB_NAME]
            collection = db[COMPANY_COLLECTION]
            
            result = collection.bulk_write(operations)
            operations.clear()
            logger.info(f'Added {BULK_SIZE} documents to database.')
            return result
        except Exception as e:
            logger.error(f'Error storing company document ({ticker}) in database.')
            logger.error(e)
            return None
    
    return f'Ticker ({ticker}) added to bulk operations list ({len(operations)} / {BULK_SIZE})...'
    
        
    