from azure.storage.blob import BlobServiceClient

class azure_storage:
    def azure_storage(self):
            try:
                sas_token = "########"
                blob_service_client = BlobServiceClient(account_url="https://adlscls.blob.core.windows.net/", credential=sas_token)
                return blob_service_client
            except(Exception) as exc:            
                return str(exc.msg)