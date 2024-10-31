from pymongo import MongoClient
import datetime

COLLECTION_COMPANY = 'companies'
COLLECTION_TICKER = 'tickers'

def transfer_documents(source_db_name='prod_db', target_db_name='test_db', limit=100, reset_coll=False):
    
    # Ask user if they are sure they want to reset the collection
    print("This will reset the target collection. Are you sure you want to continue?")
    response = input("Enter 'yes' to continue: ")
    if response.lower() != 'yes':
        print("Exiting...")
        return
    
    start = datetime.datetime.now()
    
    # Create a MongoClient
    client = MongoClient('mongodb://localhost:27017/')
    
    # check if target_db_name contains prod string and raise an error
    if 'prod' in target_db_name:
        raise ValueError("Cannot transfer data to a production database.")
    
    # Access the source and target databases
    source_db = client[source_db_name]
    target_db = client[target_db_name]
    
    # Access the collection from the source database
    source_company_collection = source_db[COLLECTION_COMPANY]
    
    # Query to find the top documents with the highest 'marketCap'
    documents = list(source_company_collection.find().sort('info.marketCap.Values', -1).limit(limit))
    tickers = []
    for company in documents:
        print(f"MarketCap: {company['info']['marketCap']['Values'][-1]} Ticker: {company['ticker']} Company: {company['info']['shortName']['Values'][-1]}")
        tickers.append(company['ticker'])
    
    # Access the collection in the target database
    target_company_collection = target_db[COLLECTION_COMPANY]
    target_tickers_collection = target_db[COLLECTION_TICKER]
    if reset_coll:
        target_company_collection.drop()
        target_tickers_collection.drop()
        print(f"Collections {COLLECTION_COMPANY} and {COLLECTION_TICKER} dropped.")
    
    # Insert documents into the target collection
    if documents:
        result = target_company_collection.insert_many(documents)
        print(f"Inserted {len(result.inserted_ids)} documents.")
    else:
        print("No copmany documents to transfer.")
        
    if len(tickers) > 0:
        document = {COLLECTION_TICKER: tickers}
        result = target_tickers_collection.insert_one(document)
        print("Tickers inserted.")
    
        
    end = datetime.datetime.now()
    print(f"Done\nTime taken: {end - start}")


# Example usage
transfer_documents(source_db_name='prod_db', target_db_name='test_db', reset_coll=True)

