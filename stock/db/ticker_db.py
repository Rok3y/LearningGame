import scrape as sc
import pandas as pd
from logging_config import logger
import db.db_common as dbc

TICKER_COLLECTION = 'tickers'

def get_tickers() -> pd.Series:
    logger.info('Getting tickers from database.')
    client = dbc.get_db_client()
    db = client[dbc.DB_NAME]
    collection = db[TICKER_COLLECTION]
    
    # Retrieve ticker document
    tickers_doc = collection.find_one({})
        
    # Check if there is any data in the database
    if tickers_doc is None:
        logger.warning(f"Cannot find any {TICKER_COLLECTION} documents.")
        return None
    
    # Convert to pandas Series
    #return pd.Series([doc['symbol'] for doc in tickers_doc])
    return pd.Series(tickers_doc["tickers"])


def add_tickers_symbol(tickers: dict):
    logger.debug(f'Storing ticker symbols ({len(tickers)}) in database.')
    try:
        client = dbc.get_db_client()
        db = client[dbc.DB_NAME]
        collection = db[TICKER_COLLECTION]
        
        # Convert the tickers dictionary to a list of ticker symbols
        tickers_list = list(tickers.values())

        # Create a document with a list of tickers
        document = {TICKER_COLLECTION: tickers_list}        
        collection.insert_one(document)
    except Exception as e:
        logger.error(f'Error storing ticker ({len(tickers)}) document in database.')
        logger.error(e)
    
    logger.debug(f'Stored ({len(tickers)}) in database.')