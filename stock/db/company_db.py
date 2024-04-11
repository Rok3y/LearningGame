import scrape as sc
import pandas as pd
import logging
import db.db_common as dbc

COMPANY_COLLECTION = 'companies'

def get_company_document(ticker: str):
    logging.debug(f'Get company document ({ticker}) from database.')
    client = dbc.get_db_client()
    db = client['stock']
    collection = db[COMPANY_COLLECTION]
    
    collection = collection.find_one({'ticker': ticker})
    if collection is None:
        logging.warning(f'Company document ({ticker}) not found in database.')
    
    return collection

def add_company_document(document: dict):
    ticker = document["ticker"]
    logging.debug(f'Storing company document ({ticker}) in database.')
    try:
        client = dbc.get_db_client()
        db = client['stock']
        collection = db[COMPANY_COLLECTION]
        
        collection.insert_one(document)
    except Exception as e:
        logging.error(f'Error storing company document ({ticker}) in database.')
        logging.error(e)
    
    logging.debug(f'Company document ({ticker}) stored in database.')

def update_company_document(document: dict):
    ticker = document["ticker"]
    logging.debug(f'Updating company document ({ticker}) in database.')
    try:
        client = dbc.get_db_client()
        db = client['stock']
        collection = db[COMPANY_COLLECTION]
        
        collection.update_one({'ticker': ticker}, {'$set': document})
    except Exception as e:
        logging.error(f'Error updating company document ({ticker}) in database.')
        logging.error(e)
    
    logging.debug(f'Company document ({ticker}) updated in database.')