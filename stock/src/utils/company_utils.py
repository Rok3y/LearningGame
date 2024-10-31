import src.utils.utils as utils
import bson

def get_latest_info(company: dict) -> tuple[dict, int]:
    '''
    Gets the latest info from the company document.
        
    Args:
    company (dict): dictionary containing the company document.

    Returns:
    tuple[dict, int]: A tuple containing the latest info and the size of the document.
    '''
    # Calculate the size of the document
    document_size = utils.bytes_to_megabytes(len(bson.encode(company)))
    
    # Get the ticker directly since it's not nested
    if 'info' in company:
        ticker = company.get('ticker', 'N/A')
    
    # initialize a dictionary to store the latest info
    latest_info = {}
    
    # check if 'info' is present and is a dictionary
    if 'info' in company and isinstance(company['info'], dict):
        # get the latest info
        for key, value_dict in company['info'].items():
            # Ensure that 'Values' is present and is a list with a lest one item
            if 'Values' in value_dict and value_dict['Values']:
                # Get the last item from the 'Values' list
                latest_info[key] = value_dict['Values'][-1]
            else:
                latest_info[key] = 'N/A'
    else:
        latest_info = 'No info available'
    
    if 'history' in company:
        history = company.get('history', 'N/A')
    else:
        history = []
        
    company_document = {
        'ticker': ticker,
        'info': latest_info,
        'history': history,
        'document_size': document_size
    }
    
    return company_document, document_size