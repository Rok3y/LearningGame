import db.company_db as cdb
import db.ticker_db as tdb

# Ticker database functions
def get_tickers():
    return tdb.get_tickers()

def add_tickers_symbol(tickers: dict):
    return tdb.add_tickers_symbol(tickers)

# Company database functions
def get_company_document(ticker: str):
    return cdb.get_company_document(ticker)

def add_company_document(document: dict):
    return cdb.add_company_document(document)

def update_company_document(document: dict):
    return cdb.update_company_document(document)

def add_or_update_company_document(document: dict):
    return cdb.add_or_update_company_document(document)