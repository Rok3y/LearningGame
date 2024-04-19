import yfinance as yf
import src.db.database as db
import src.scrape as sc 
import pandas as pd
import asyncio
import aiohttp
import click
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from queue import Queue
from datetime import datetime, timedelta
from time import sleep
import src.sync_data_service as sds
from src.logging_config import logger

# An example of using yFinance to get stock data
# https://algotrading101.com/learn/yfinance-guide/

def update_ticker_list():
    # Get all tickers
    tickers = db.get_tickers()
    if tickers is None:
        tickers = pd.Series([])
    
    logger.info(f"found {len(tickers)}")
    
    logger.info("Fetching tickers...")
    scraped_tickers = sc.get_all_tickers()
    new_tickers = scraped_tickers[~scraped_tickers.isin(tickers)]
    if len(new_tickers) == 0:
        logger.info("No new tickers found.")
        return
    
    db.add_tickers_symbol(new_tickers.to_list())
    logger.info(f"Updated {len(new_tickers)} tickers.")
    
@click.command()
@click.option('--update-tickers', is_flag=True, help="Update tickers in database")
def main(update_tickers: bool):
    
    start_time = datetime.now()
    if update_tickers:
        update_ticker_list()
        
    # Get all tickers
    #tickers = db.get_tickers()
    tickers = sc.get_top_100_tickers()[:10]
    
    if tickers is None or len(tickers) == 0:
        logger.error("No tickers found in database.")
        return
    
    ticker_counter = 0
    # Get ticker data from database and check for new data
    for ticker in tickers:        
        sds.update_or_init_collection(ticker)
        ticker_counter += 1
        logger.info(f"{ticker_counter}/{len(tickers)} Ticker: {ticker} done! ")
        
    # Since we wait for at least 100 documents before we bulk insert, we need to check if we have any operations left and insert them
    db.add_or_update_company_document_bulk(document = None, update_remaining=True)
    
    # with ThreadPoolExecutor(max_workers=32) as executor:
    #     executor.map(update_or_init_collection, tickers)

    # Mutli-threaded version
    # for ticker in tickers:
    #     process_dl_queue.put(ticker)
    
    # num_dl_threads = 16
    # for _ in range(num_dl_threads):
    #     t = Thread(target=get_db_and_scraped_data)
    #     t.start()
        
    # t2 = Thread(target=update_or_init_company_collection)
    # t2.start()
    
    # process_dl_queue.join()
    # process_db_queue.put((None, None, None)) # This indicates that download/scraped queue is done and we can send the end signal (poison pill)
    # t2.join()
    
    # Example with two threads (put and pop from queue)
    # t1 = Thread(target=get_db_and_scraped_data, args=(tickers,))
    # t2 = Thread(target=update_or_init_company_collection)
    # t1.start()
    # t2.start()
    # t1.join()
    # t2.join()
    
    # Get time needed to update data
    end_time = datetime.now()
    logger.info(f"Time taken: {end_time - start_time}s")
    
    # Get all failed tickers
    ticker_failed = list(set(tickers) - set(sds.ticker_processed_succesfully))
    logger.info(f"Failed to process tickers: {ticker_failed}")
    
    logger.info("Done!")

if __name__ == '__main__':    
    main()
    
    