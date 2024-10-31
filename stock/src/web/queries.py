import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
sys.path.insert(0, project_root)
from src.logging_config import logger
import src.db.db_common as dbc

collection = dbc.MongoDBManager.get_company_collection()

def get_company_document(ticker: str):
    logger.debug(f'Get company document ({ticker}) from database.')
    
    try:
        document = collection.find_one({'ticker': ticker})
        if collection is None:
            logger.warning(f'Company document ({ticker}) not found in database.')
    except Exception as e:
        logger.error(f'Error getting company document ({ticker}) from database.')
        logger.error(e)
    
    return document

def find_companies(query: dict, prjection: dict = None):
    logger.debug('Get all company documents from database.')
    
    try:
        documents = collection.find(query, prjection)
        if documents is None:
            logger.warning('Company documents not found in database.')
    except Exception as e:
        logger.error('Error getting company documents from database.')
        logger.error(e)
    
    return documents

def aggregate_companies(pipeline: list):
    logger.debug('Aggregate company documents from database.')
    
    try:
        documents = collection.aggregate(pipeline)
        if documents is None:
            logger.warning('Company documents not found in database.')
    except Exception as e:
        logger.error('Error aggregating company documents from database.')
        logger.error(e)
    
    return documents