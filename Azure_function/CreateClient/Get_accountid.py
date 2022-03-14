from wsgiref import headers
import requests
import json
import base64

class SalesforceConfig:
    def __init__(self):
        self.params = {
            "client_id" : "#######",
            "client_secret" : "######",
            "username" : "USER_NAME",
            "password" : "#######",
            "grant_type" : "password"
        }

        self.r = requests.post("https://login.salesforce.com/services/oauth2/token",params=self.params)
        self.access_token = self.r.json().get("access_token")
        self.instance_url = self.r.json().get("instance_url")

        # print("instance_url",self.instance_url)
        # print("access_token",self.access_token)
    
    def sf_call_acc_id(self,action,method='get'):
        headers={
            'Content_type' : 'application/json',
            'Accept_Encoding' : 'gzip',
            'Authorization' : 'Bearer '+self.access_token
        }
        
        if method=='get':
            r = requests.request(method,self.instance_url+action,headers=headers,timeout=30)
        elif method in['post','patch']:
            r = requests.request(method,self.instance_url+action,headers=headers,timeout=10)
        else:
            raise ValueError('Method be should either get or post or patch')                
        
        if r.status_code<300:
            if method=='patch':
                return None
            else:
                return r.json()
        else:
            raise Exception("API error with calling URL",r.json())
