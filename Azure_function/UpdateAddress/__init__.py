import logging
from .database_op import Database_op
import json
import azure.functions as func
from .SalesforceUpdate import SalesforceConfig

database_obj = Database_op()
salesConfig_obj = SalesforceConfig()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        Api_key = req.headers.get('Api-access-token')        
        print(Api_key)
        verify_status = database_obj.verify_api_key(Api_key)        
        if verify_status == 1:
            ClientId = req.params.get('ClientId')    
            Address1 = req.params.get('Address1')
            Suburb = req.params.get('Suburb')
            PostCode = req.params.get('PostCode')
            State = req.params.get('State')
            Country = req.params.get('Country')
            
            if (not ClientId) and (not Address1) and (not Suburb) and (not PostCode) and (not State) and (not Country):
                try:
                    req_body = req.get_json()
                except ValueError:
                    pass
                else:
                    ClientId = req_body.get('ClientId')    
                    Address1 = req_body.get('Address1')
                    Suburb = req_body.get('Suburb')
                    PostCode = req_body.get('PostCode')
                    State = req_body.get('State')
                    Country = req_body.get('Country')
            
            # get API token and verify
        
            if ClientId and Address1 and Suburb and PostCode and State and Country:        
                print("ClientId:",ClientId)
                print("Address1:",Address1)
                print("Suburb:",Suburb)
                print("PostCode:",PostCode)
                print("State:",State)
                print("Country:",Country)
                
                # Get account id                
                accountid = database_obj.get_acc_id(ClientId)
                
                if accountid == None:
                    return func.HttpResponse(f"No record found for ClientId: {ClientId}", status_code=400)
                
                # Get contact id
                oportunitydata = json.dumps(salesConfig_obj.sf_call_contact_id("/services/data/v20.0/query/?q=SELECT+id+from+Contact+where+account.id='"+accountid+"'"))       
                dict_data = json.loads(oportunitydata)            
                contact_id = dict_data["records"][0]["Id"]                     
                print(contact_id)
                
                # Call contact API to store address in salesforce
                data1 = {   
                "AssistantName": ClientId,
                "MailingState" : State,
                "MailingCity": Suburb,
                "MailingStreet": Address1,
                "MailingCountry": Country,
                "MailingPostalCode": PostCode
                }
                
                try:
                    oportunitydata = json.dumps(salesConfig_obj.sf_call('/services/data/v54.0/sobjects/Contact/'+contact_id,data=data1,method="patch"),indent=4,sort_keys=True)
                    print(oportunitydata)
                except Exception as e:            
                    return func.HttpResponse(f"Error in Adding address: {e}", status_code=400)
                
                msg = database_obj.insert_data(Address1, Suburb, State, PostCode, Country, ClientId)
                return func.HttpResponse(msg, status_code=200)
            else:
                return func.HttpResponse(
                    "This HTTP triggered function executed successfully. Pass a valid key in the query string or in the request body for a personalized response.",
                    status_code=200
                )
        else:
            return func.HttpResponse("Authorization failed", status_code=400)
    except Exception as e:
        return func.HttpResponse(f"Error in Adding address: {e}", status_code=400)
