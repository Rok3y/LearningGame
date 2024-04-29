import src.db.database as db
import src.scrape as sc 
import pandas as pd
import click
import src.sync_data_service as sds
import datetime
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
    
    logger.info("Starting stock update...")
    start_time = datetime.now()
    if update_tickers:
        update_ticker_list()
        
    # Get all tickers
    tickers = db.get_tickers()
    #tickers = sc.get_top_100_tickers()[:10]
    
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
    # Get time needed to update data
    end_time = datetime.now()
    logger.info(f"Time taken: {end_time - start_time}s")
    
    # Get all failed tickers
    ticker_failed = list(set(tickers) - set(sds.ticker_processed_succesfully))
    logger.info(f"Failed to process tickers: {ticker_failed}")
    
    logger.info("Done!")

if __name__ == '__main__':    
    main()
    
    