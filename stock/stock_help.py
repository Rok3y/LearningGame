import yfinance as yf
import database as db
import scrape as sc 
import pandas as pd
import asyncio
import aiohttp
import click
import logging
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue
from datetime import datetime, timedelta


def update_or_init_collection_old(ticker: str, exclude_attrs: list = ['companyOfficers', 'longBusinessSummary']):
    '''
        Update or initialize a collection for a given ticker
        :param ticker: str
        :param exclude_attrs: list
        :return: dict
    '''
    logging.info(f"Updating company document ({ticker})...")
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # Get current data (data from database and scraped data) and update db data with new data
    company_dict = db.get_company_document(ticker)
    yf_ticker = yf.Ticker(ticker)
    if yf_ticker is None:
        logging.warning(f"Ticker {ticker} not found in Yahoo Finance")
        return
    new_collection = yf_ticker.info
    if not len(new_collection.keys()) > 1:
        logging.warning(f"Ticker {ticker} does not have any data")
        return
    
    # Check if the collection exists
    if company_dict is None or len(company_dict) == 0:
        logging.debug(f'Company document ({ticker}) is empty, creating new document')
        company_dict = {
        'ticker': ticker,
        'info': {},
        'history': []
    }

    # Check for changes in the info collection
    for attr_name, attr_value in new_collection.items():
        # Exclude specified attributes
        if attr_name in exclude_attrs:
            continue
        
        # Check if the attribute already exists
        if attr_name in company_dict['info']:
            # Update existing attribute
            # Check if new attribute value is different from the current one
            if attr_value != company_dict['info'][attr_name]['Values'][-1]:
                logging.debug(f"{attr_name}: old value {company_dict['info'][attr_name]["Values"][-1]} --> new value: {attr_value}")
                company_dict['info'][attr_name]['Dates'].append(current_date)
                company_dict['info'][attr_name]['Values'].append(attr_value)
        else:
            # Initialize new attribute
            company_dict['info'][attr_name] = {
                'Dates': [current_date],
                'Values': [attr_value]
            }
    
    # Check for changes in the history collection
    history_data_dict = None
    if company_dict['history'] is None or len(company_dict['history']) == 0:
        history_data_dict = yf_ticker.history(period="max", interval="1d").to_dict()
    else:
        # Get last date in the history collection and get new data from that date
        last_date = datetime.strptime(company_dict['history'][-1]['Date'], '%Y-%m-%d %H:%M:%S')
        last_date = last_date + timedelta(days=1) # increment by one day
        if last_date.date() <= datetime.now().date():
            history_data_dict = yf_ticker.history(start=last_date.strftime('%Y-%m-%d'), interval="1d").to_dict()
        else:
            logging.info(f"History data for {ticker} is up to date.")
        
    # Check if history data is available
    if history_data_dict is not None and len(history_data_dict) > 0:
        # Add history data to the collection
        history_data_list = convert_history_data_to_list(history_data_dict)
        company_dict['history'].extend(history_data_list)
    
    # Add or update collection in database
    result = db.add_or_update_company_document(company_dict)
    # logging.info(f"Changes made to company document ({ticker}) : {changes}")
    if result.upserted_id is not None:
        print("Upserted ID:", result.upserted_id)
    else:
        logging.info(f"No changes made to company document ({ticker})")
        
    ticker_processed_succesfully.append(ticker)
    return company_dict