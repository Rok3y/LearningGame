import db.db_common as dbc
import company_utils
import utils
import json

# test if database is properly populed
# get all documents from companies collection and check you attribute values if it exists

client = dbc.MongoDBClient.get_client()
db = client[dbc.DB_NAME]
company_collection = db['companies']

# Define the expected schema as a set of keys
expected_company_keys = {'_id', 'ticker', 'info', 'history'}

# Get database stats
stats = db.command("dbstats")

# Print relevant data
print(f"Data Size: {utils.bytes_to_megabytes(stats['dataSize']):.2f} MB") # the total size of the data held in the database
print(f"Storage Size: {utils.bytes_to_megabytes(stats['storageSize']):.2f} MB") # the total amount of space allocated to collections for storing this data

# Function to compare document schema
def check_schema(document, expected_keys):
    return set(document.keys()) == expected_keys

def test_all_company_documents_schema():
    # Fetch all documents
    documents = company_collection.find({})
    
    # Check each document
    all_match = True
    for doc in documents:
        if not check_schema(doc, expected_company_keys):
            all_match = False
            print(f"Document {doc['_id']} does not match the expected schema.")
            break

    if all_match:
        print("All documents match the expected schema.")

def test_all_company_documents(exclude_history: bool = False):
    # Count documents (use this if you want to count without retrieving all data)
    num_companies = company_collection.count_documents({})
    print(f"Number of companies: {num_companies}")
    
    exclusion = {}
    if exclude_history:
        exclusion = {'ticker': 1, 'info': 1}
        
    copmanies_res = company_collection.find({}, exclusion)
    # Get explanation for the same query
    explanation = company_collection.find({}).explain()
    
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
        
    print(json.dumps(explanation, indent=4))
        

test_all_company_documents_schema()
test_all_company_documents()

#company_collection.create_index([('ticker', 1)], unique=True) # create index on 'ticker' field