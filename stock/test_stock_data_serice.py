import db.db_common as dbc
import company_utils
import utils

# test if database is properly populed
# get all documents from companies collection and check you attribute values if it exists

client = dbc.get_db_client()
db = client['stock']
company_collection = db['companies']

# Get database stats
stats = db.command("dbstats")

# Print relevant data
print(f"Data Size: {utils.bytes_to_megabytes(stats['dataSize']):.2f} MB") # the total size of the data held in the database
print(f"Storage Size: {utils.bytes_to_megabytes(stats['storageSize']):.2f} MB") # the total amount of space allocated to collections for storing this data

def test_all_company_documents(exclude_history: bool = False):
    # Count documents (use this if you want to count without retrieving all data)
    num_companies = company_collection.count_documents({})
    print(f"Number of companies: {num_companies}")
    
    if exclude_history:
        copmanies_res = company_collection.find({}, {'ticker': 1, 'info': 1}) # only retrieve the 'ticker' and 'info' fields and exclude history
    else:
        copmanies_res = company_collection.find({})
    
    for company in copmanies_res:
        
        company_latest, doc_size = company_utils.get_latest_info(company)
        ticker = company_latest.get('ticker', 'N/A')
        
        # prepare strings for display based on the latest info retrieved
        name = company_latest['info'].get('shortName', 'N/A')
        sector = company_latest['info'].get('sector', 'N/A')
        industry = company_latest['info'].get('industry', 'N/A')
        num_employees = company_latest['info'].get('fullTimeEmployees', 'N/A')
        history_included = 'history' in company and len(company['history']) > 0
        print(f"History: {history_included} # Company:  {doc_size:.2f} MB -- ({ticker}) name: {name} sector: {sector} industry: {industry} employees: {num_employees}")
        

test_all_company_documents()