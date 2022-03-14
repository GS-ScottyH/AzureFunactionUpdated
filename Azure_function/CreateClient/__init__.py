import logging
from .database_op import Database_op
import azure.functions as func
import json
from .Get_accountid import SalesforceConfig

database_obj = Database_op()
salesforce_obj = SalesforceConfig()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # If the request is a GET request, then fetch the data from the database.
        if req.method == "GET":
            data = database_obj.get_data()
            return func.HttpResponse(f"{data}")
                    
        # If the request is a POST request, then insert the data into the database.
        else: 
            account_number = req.params.get('accountnumber')
            name = req.params.get('name')
            lastmodifieddate = req.params.get('lastmodifieddate')
            
            if (not name) and (not account_number):
                try:
                    req_body = req.get_json()
                except ValueError:
                    pass
                else:
                    name = req_body.get('name')
                    account_number = req_body.get('accountnumber')
                    lastmodifieddate = req_body.get('lastmodifieddate')                    

            if name and account_number and lastmodifieddate:
                
                oportunitydata = json.dumps(salesforce_obj.sf_call_acc_id("/services/data/v20.0/query/?q=SELECT+id+from+Account+where+name='"+name+"'"))
                dict_data = json.loads(oportunitydata)            
                account_id = dict_data["records"][0]["Id"]                     
                
                print(name,account_number,account_id)
                result = database_obj.check_accnumber(account_number)
                if result==None:
                    msg = database_obj.insert_data(account_number, name,account_id, lastmodifieddate)
                else:
                    msg = database_obj.update_record(account_number, name)                
                return func.HttpResponse(f"{msg}")
            else:
                return func.HttpResponse(
                    "Please enter name and accountnumber in the query string or in the request body.",status_code=200
                )
    
    except Exception as e:
        print(f"{e}")
        return func.HttpResponse(f"{e}")