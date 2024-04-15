import scrape as sc
import pandas as pd
from logging_config import logger
import db.db_common as dbc
#logger = logging.getLogger('StocksLogger')

COMPANY_COLLECTION = 'companies'

def get_company_document(ticker: str):
    logger.debug(f'Get company document ({ticker}) from database.')
    client = dbc.get_db_client()
    db = client[dbc.DB_NAME]
    collection = db[COMPANY_COLLECTION]
    
    collection = collection.find_one({'ticker': ticker})
    if collection is None:
        logger.warning(f'Company document ({ticker}) not found in database.')
    
    return collection

def add_company_document(document: dict):
    ticker = document["ticker"]
    logger.debug(f'Storing company document ({ticker}) in database.')
    try:
        client = dbc.get_db_client()
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
        client = dbc.get_db_client()
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
        client = dbc.get_db_client()
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
    
    logger.debug(f'Company document ({ticker}) stored in database.')
    return result