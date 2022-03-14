import logging
from .Azure_storage import azure_storage
import azure.functions as func
from .database_op import Database_op

azure_obj = azure_storage()
database_obj = Database_op()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:  
        Api_key = req.headers.get('Api-access-token')        
        print(Api_key)            
        verify_status = database_obj.verify_api_key(Api_key)        
        if verify_status == 1:  
            file1 = req.files['file1']
            file2 = req.files['file2']    
            referralCode  = req.form['referralCode']
            fileCount  = req.form['fileCount']
            accountid = req.form['accountid']
            if (not file2) and (not file1) and (not referralCode) and (not fileCount):
                try:
                    req_body = req.get_json()
                except ValueError:
                    pass
                else:
                    accountid = req_body.get('accountid')
                    file1 = req_body.get('file1')
                    file2 = req_body.get('file2')
                    referralCode = req_body.get('referralCode')
                    fileCount = req_body.get('fileCount') 
            
            if referralCode == 'GSMB':               
                blob_service_client=azure_obj.azure_storage()
                
                #Upload file1 to Azure Blob Storage
                blob_client = blob_service_client.get_blob_client(container="salesforce", blob="/"+accountid+"/"+file1.filename)
                blob_client.upload_blob(file1,overwrite=True)
                
                #Upload file2 to Azure Blob Storage
                blob_client_ = blob_service_client.get_blob_client(container="salesforce", blob="/"+accountid+"/"+file2.filename)
                blob_client_.upload_blob(file2,overwrite=True)
                
            else:
                return func.HttpResponse("Invalid Referral Code", status_code=400)
            
            
            if referralCode and file1 and file2 and fileCount:
                return func.HttpResponse("File inserted successfully", status_code=200)
            else:
                return func.HttpResponse(
                    "This HTTP triggered function executed successfully. Pass a valid key in the query string or in the request body for a personalized response.",
                    status_code=400
                )
        else:
            return func.HttpResponse("Authorization failed", status_code=400)
            
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)