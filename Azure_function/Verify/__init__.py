import logging
import json
import azure.functions as func
import requests


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Initiate session
        headers = {
                        'accept': 'application/json',  
                        'content-type' : 'application/json',
                        'accept-encoding' : 'gzip,deflate,br',  
                    }

        response = requests.post('https://dashboard-test.proviso.com.au/api/scv/v1/init/gsmb', headers=headers)
        print(response.json()['sessionToken'])
        session_token = response.json()['sessionToken'] #This session token is used to login and select accounts        

        # Login 
        headers = {
                        'accept': 'application/json',  
                        'content-type' : 'application/json',
                        'accept-encoding' : 'gzip,deflate,br', 
                        'x-session-token': session_token
                    }

        data = {
                "credentials": {
                                    "institution": "bank_of_statements",
                                    "username": "12345678",
                                    "password": "TestMyMoney"
                                }
                }

        response = requests.post('https://dashboard-test.proviso.com.au/api/scv/v1/login', headers=headers ,data = json.dumps(data))
        login_status = response.json()['success']
        print(login_status)

        if login_status==True:
            # SelectAccounts
            headers = {
                        'accept': 'application/json',  
                        'content-type' : 'application/json',
                        'accept-encoding' : 'gzip,deflate,br', 
                        'x-session-token': session_token
                    }

            data = {
                    "accounts": {
                                    "bank_of_statements": [0,1,2]
                                }
                    }
            
            response = requests.post('https://dashboard-test.proviso.com.au/api/scv/v1/selectAccounts', headers=headers ,data = json.dumps(data))
            login_status = response.json()['success']
            account_status = response.json()['accountsSelectionSubmitted']
            print(login_status,account_status)
            
            if login_status==True and account_status==True:
                # Finished session
                headers = {
                        'accept': 'application/json',  
                        'content-type' : 'application/json',
                        'accept-encoding' : 'gzip,deflate,br', 
                        'x-session-token': session_token
                    }
                
                response = requests.post('https://dashboard-test.proviso.com.au/api/scv/v1/finished', headers=headers)                
                return func.HttpResponse("Account verified", status_code=200)
            else:
                return func.HttpResponse("Login failed", status_code=400)
        else:
            return func.HttpResponse("Login failed", status_code=400)

    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)