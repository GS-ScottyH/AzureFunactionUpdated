import logging
import azure.functions as func
import os
import requests
import xmltodict
from .database_op import Database_op
from .Azure_storage import azure_storage

database_obj = Database_op()
azure_obj = azure_storage()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        accountid = req.params.get('accountid')
        if not accountid:
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:
                accountid = req_body.get('accountid')

        url="https://test-au.vixverify.com/Registrations-Registrations/DynamicFormsServiceV3"
        headers = {'content-type': 'text/xml'}
        body = """<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:dyn="http://dynamicform.services.registrations.edentiti.com/">
            <soapenv:Header/>
            <soapenv:Body>
                <dyn:registerVerification>
                    <accountId>gsm_anz</accountId>
                    <password>XyL-x9d-ErZ-uD7</password>
                    <verificationId/>
                    <ruleId>default</ruleId>
                    <name>
                        <honorific/>
                        <givenName>John</givenName>
                        <middleNames>TWOPASS</middleNames>
                        <surname>SMITH</surname>
                    </name>
                    <email></email>
                    <currentResidentialAddress>
                        <country>AU</country>
                        <flatNumber/>
                        <streetNumber>1</streetNumber>
                        <streetName>King</streetName>
                        <streetType>St</streetType>
                        <suburb>Melbourne</suburb>
                        <state>VIC</state>
                        <postcode>3000</postcode>
                    </currentResidentialAddress>
                    <dob>
                        <day>14</day>
                        <month>09</month>
                        <year>1977</year>
                    </dob>
                    <homePhone/>
                    <workPhone/>
                    <mobilePhone/>
                    <deviceIDData/>
                    <generateVerificationToken>true</generateVerificationToken>
                    <extraData>
                        <name>dnb-credit-header-consent-given</name>
                        <value>true</value>
                    </extraData>
                    <extraData>
                        <name>driversLicenceState</name>
                        <value>VIC</value>
                    </extraData>
                    <extraData>
                        <name>driversLicenceNumber</name>
                        <value>11111111</value>
                    </extraData>
                </dyn:registerVerification>
            </soapenv:Body>
        </soapenv:Envelope>
        """

        response = requests.post(url,data=body,headers=headers)
        stack_d = xmltodict.parse(response.content)

        status = stack_d['env:Envelope']['env:Body']['ns2:registerVerificationResponse']['return']['verificationResult']['overallVerificationStatus']
        if status == 'VERIFIED':
            
            print('Verification Successful')
            # Write response in xml.file
            file_name = "Bankstatement.xml"
            
            # f = open(file_name, "wb")
            # f.write(response.content)
            # f.close()
            
            # Database column update
            database_obj.update_varified_status(accountid,"YES")
            
            # open and store file in Azure storade
            # f = open(file_name, "r")    
            blob_service_client = azure_obj.azure_storage()
            blob_client_ = blob_service_client.get_blob_client(container="salesforce", blob="/"+accountid+"/"+file_name)
            blob_client_.upload_blob(response.content,overwrite=True)
            # f.close()
            
            # Delete the file
            # os.remove(file_name)
            return func.HttpResponse("Verification successful", status_code=200)        
        else:
            return func.HttpResponse("Verification Failed", status_code=400)
    
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)    
        