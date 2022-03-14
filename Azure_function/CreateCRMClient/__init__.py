import logging
# from .database_op import Database_op
import azure.functions as func
from .SalesforceUpdate import SalesforceConfig
import json

# database_obj = Database_op()
salesConfig_obj =SalesforceConfig()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:        
        account_number = req.params.get('accountnumber')
        name = req.params.get('name')
        
        if (not name) and (not account_number):
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                name = req_body.get('name')
                account_number = req_body.get('accountnumber')

        if name and account_number:
            # msg = database_obj.insert_data(account_number, name)                
            data1 = {
            "Name" : name,
            "AccountNumber" : account_number
            }
            oportunitydata = json.dumps(salesConfig_obj.sf_call('/services/data/v53.0/sobjects/Account/',data=data1,method="post"),indent=4,sort_keys=True)                
            return func.HttpResponse(f"{oportunitydata}")
            # return func.HttpResponse(f"{oportunitydata}")
        else:
            return func.HttpResponse(
                "Please enter name and quantity in the query string or in the request body.",
                status_code=200
            )

    except Exception as e:
        print(f"{e}")
        return func.HttpResponse(f"{e}")


