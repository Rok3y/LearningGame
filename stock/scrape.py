import yahoo_fin.stock_info as si
import yfinance as yf
import pandas as pd
import asyncio
import aiohttp
from bs4 import BeautifulSoup

def get_all_tickers() -> pd.Series:
    print(f"Scraping all tickers...")
    dow_list = si.tickers_dow()
    #ftse100_list = si.tickers_ftse100() # error
    #ftse250_list = si.tickers_ftse250() # error
    ibovespa_list = si.tickers_ibovespa()
    nasdaq_list = si.tickers_nasdaq() # 4954
    nifty50_list = si.tickers_nifty50()
    niftybank_list = si.tickers_niftybank()
    other_list = si.tickers_other()
    sp500_list = si.tickers_sp500()

    # combine all lists and do not allow duplicates
    all_tickers = list(set(dow_list + nasdaq_list + nifty50_list + niftybank_list + other_list + sp500_list + ibovespa_list))
    print(f"Scrapped {len(all_tickers)} tickers")
    
    # convert to pandas series
    all_tickers = pd.Series(all_tickers)

    return all_tickers

def get_top_100_tickers() -> pd.Series:
    return pd.Series([
    "MSFT", "AAPL", "NVDA", "2222.SR", "AMZN", "GOOG", "META", "BRK-B", "TSM", "LLY",
    "AVGO", "JPM", "V", "NVO", "TSLA", "WMT", "XOM", "MA", "MC.PA", "UNH",
    "005930.KS", "ASML", "JNJ", "TCEHY", "PG", "HD", "ORCL", "TM", "MRK", "COST",
    "CVX", "ABBV", "BAC", "CRM", "600519.SS", "NFLX", "AMD", "NESN.SW", "RMS.PA", "KO",
    "601857.SS", "1398.HK", "RELIANCE.NS", "IHC.AE", "OR.PA", "PEP", "SHEL", "SAP", "LIN", "TMO",
    "ADBE", "DIS", "ACN", "AZN", "601288.SS", "WFC", "CSCO", "NVS", "MCD", "ROG.SW",
    "QCOM", "ABT", "0941.HK", "CAT", "TMUS", "DHR", "BABA", "INTU", "VZ", "AMAT",
    "IBM", "TCS.NS", "TTE", "GE", "601988.SS", "INTC", "CMCSA", "AXP", "NOW", "601939.SS",
    "COP", "UBER", "HSBC", "TXN", "IDEXY", "PDD", "MS", "PFE", "BHP", "SIE.DE",
    "HDB", "UNP", "CDI.PA", "AIR.PA", "RY", "AMGN", "PRX.AS", "MU", "PM", "SPGI"
    ])
    

async def get_stock_summary(ticker: str) -> pd.DataFrame:
    ''' Fetch stock summary '''
    print(f"Scraping {ticker} summary...")
    info = yf.Ticker(ticker)
    return pd.DataFrame(info.info, index=[ticker])

async def get_all_stocks_summary(tickers: pd.Series) -> pd.DataFrame:
    ''' Fetch stocks summaries '''
    tasks = []
    for ticker in tickers: #get_top_20_tickers(): 
        tasks.append(asyncio.create_task(get_stock_summary(ticker))) # create schedules all tasks to run concurrently
        #tasks.append(asyncio.create_task(get_stock_profile(ticker))) # create schedules all tasks to run concurrently
    
    # Await the completion of all get summary tasks
    results_summary = await asyncio.gather(*tasks)
    
    # 
    
    # Filter results to get only successful responses
    filtered_results = {ticker: dict_res for ticker, dict_res, response_code in results_summary if response_code == 200}
    
    return filtered_results

# start_time = datetime.datetime.now()

# stocks = asyncio.run(fetch_stocks())
# count = 0


# # for ticker in get_all_tickers()[:50]:
# #     count += 1

# #     if ticker != '':
# #         stock_summary, response_code = get_stock_summary(ticker)
# #         if response_code == 200 and len(stock_summary.keys()) > 0:
# #             stocks[ticker] = stock_summary
# #             print(f"{count} - {ticker}")
# #         else:
# #             print(f"Error: {ticker} - {response_code} - No data found")

# for stock in stocks:
#     if "Forward Dividend & Yield" in stocks[stock]:
#         print(f'{stock}: {stocks[stock]["Forward Dividend & Yield"]}')
#     else:
#         print(f'{stock}: No dividend')

# end_time = datetime.datetime.now()

# print(f"Time taken: {end_time - start_time}")