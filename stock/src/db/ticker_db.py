import pandas as pd
from src.logging_config import logger
import src.db.db_common as dbc


def get_tickers() -> pd.Series:
    logger.info('Getting tickers from database.')
    collection = dbc.MongoDBManager.get_ticker_collection()
    
    # Retrieve ticker document
    tickers_doc = collection.find_one({})
        
    # Check if there is any data in the database
    if tickers_doc is None:
        logger.warning(f"Cannot find any {dbc.TICKER_COLLECTION} documents.")
        return None
    
    # Convert to pandas Series
    #return pd.Series([doc['symbol'] for doc in tickers_doc])
    return pd.Series(tickers_doc["tickers"])


def add_tickers_symbol(tickers: list):
    logger.debug(f'Storing ticker symbols ({len(tickers)}) in database.')
    try:
        collection = dbc.MongoDBManager.get_ticker_collection()
        document = collection.find_one({})
        
        # get document id from the first document
        document_id = document['_id']
        
        # MongoDB update query that uses $addToSet to avoid duplicates
        update_result = collection.update_one(
            {'_id': document_id}, # Query part: find the document by id
            {'$addToSet': {'tickers': {'$each': tickers}}}, # Update part: add tickers avoiding duplicates
            upsert=True # If the document does not exist, create it
        )
    except Exception as e:
        logger.error(f'Error storing ticker ({len(tickers)}) document in database.')
        logger.error(e)
        return None
    
    if update_result.matched_count:
        logger.info(f'Updated existing document with ({len(tickers)}) tickers.')
    else:
        logger.info(f'Stored new document with ({len(tickers)}) tickers.')

    return update_result