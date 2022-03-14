import logging
import requests
# from requests.auth import HTTPBasicAuth
import json
import azure.functions as func
from .database_op import Database_op

database_obj = Database_op()

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        account_name = req.params.get('account_name')
        first_name = req.params.get('first_name')        
        last_name = req.params.get('last_name')
        # infoxchange_id = req.params.get('infoxchange_id')
        
        # account_name = req.params.get('account_name')
        # first_name = req.params.get('first_name')
        # last_name = req.params.get('last_name')        
        # azure = req.params.get('azure')
        # first_name = req.params.get('first_name')
        middle_name = req.params.get('middle_name')
        # last_name = req.params.get('last_name')
        sex = req.params.get('sex')
        gender = req.params.get('gender')    
        dob = req.params.get('dob')
        day_unknown = req.params.get('day_unknown')
        month_unknown = req.params.get('month_unknown')
        year_estimate = req.params.get('year_estimate')
        indigenous = req.params.get('indigenous')
        southsea_islander = req.params.get('southsea_islander')
        ancestry = req.params.get('ancestry')    
        cald = req.params.get('cald')
        cob = req.params.get('cob')
        year_of_arrival = req.params.get('year_of_arrival')
        month_of_arrival = req.params.get('month_of_arrival')
        language = req.params.get('language')
        english_proficiency = req.params.get('english_proficiency')
        interpreter_required = req.params.get('interpreter_required')
        title = req.params.get('title')
        position = req.params.get('position')
        organisation = req.params.get('organisation')    
        dod = req.params.get('dod')
        crn = req.params.get('crn')
        dva = req.params.get('dva')
        update_reason = req.params.get('update_reason')
        end_date = req.params.get('end_date')
        comments = req.params.get('comments')
        
        
        if (not account_name) and (not first_name) and (not last_name):
            try:
                req_body = req.get_json()
            except ValueError:
                pass
            else:         
                account_name = req_body.get('account_name')       
                first_name = req_body.get('first_name')                
                last_name = req_body.get('last_name')
                # infoxchange_id = req_body.get('infoxchange_id')

                # account_name = req_body.get('account_name')
                # first_name = req_body.get('first_name')
                # last_name = req_body.get('last_name')
                
                # azure = req_body.get('azure')
                # first_name = req_body.get('first_name')
                middle_name = req_body.get('middle_name')
                # last_name = req_body.get('last_name')
                sex = req_body.get('sex')
                gender = req_body.get('gender')    
                dob = req_body.get('dob')
                day_unknown = req_body.get('day_unknown')
                month_unknown = req_body.get('month_unknown')
                year_estimate = req_body.get('year_estimate')
                indigenous = req_body.get('indigenous')
                southsea_islander = req_body.get('southsea_islander')
                ancestry = req_body.get('ancestry')    
                cald = req_body.get('cald')
                cob = req_body.get('cob')
                year_of_arrival = req_body.get('year_of_arrival')
                month_of_arrival = req_body.get('month_of_arrival')
                language = req_body.get('language')
                english_proficiency = req_body.get('english_proficiency')
                interpreter_required = req_body.get('interpreter_required')
                title = req_body.get('title')
                position = req_body.get('position')
                organisation = req_body.get('organisation')    
                dod = req_body.get('dod')
                crn = req_body.get('crn')
                dva = req_body.get('dva')
                update_reason = req_body.get('update_reason')
                end_date = req_body.get('end_date')
                comments = req_body.get('comments')
        
        result = database_obj.check_infoxcangeid(account_name)
        
        if result==False:
            data = {
                "source_identifiers": {
                    "azure": account_name
                    },
                "first_name": first_name,
                "middle_name": middle_name,
                "last_name": last_name,
                "sex": sex,
                "gender": gender,
                "dob": dob,
                "day_unknown": day_unknown,
                "month_unknown": month_unknown,
                "year_estimate": year_estimate,
                "indigenous": indigenous,
                "southsea_islander": southsea_islander,
                "ancestry": ancestry,
                "cald": cald,
                "cob": cob,
                "year_of_arrival": year_of_arrival,
                "month_of_arrival": month_of_arrival,
                "language": language,
                "english_proficiency": english_proficiency,
                "interpreter_required": interpreter_required,
                "title": title,
                "position": position,
                "organisation": organisation,
                "dod": dod,
                "crn": crn,
                "dva": dva,
                "update_reason": update_reason,
                "end_date": end_date,
                "comments": comments
            }

            headers = {
                'accept': 'application/json',  
                'content-type' : 'application/json',
                'accept-encoding' : 'gzip,deflate,br',  
            }
            
            try:
                response = requests.post('https://srs-goodshepherd-uat.infoxchangeapps.net.au/api/v1/clients', auth = ('YSB0ZXN0aW5nIGVudmlyb25tZW50', 'Z29vZCBzaGVwaGVyZCBhcGkgdXNlcg=='), headers=headers ,data = json.dumps(data))            
                infoxchange_id = response.json()['client_id']            
            except Exception as e:
                return func.HttpResponse(response.json()['error']['message'],status_code=response.json()['http_status'])
            
            msg = database_obj.insert_data(account_name,first_name,last_name,infoxchange_id)
        
        else:            
            msg = database_obj.update_data(account_name,first_name,last_name)

        if account_name and first_name and last_name and infoxchange_id:
            return func.HttpResponse(msg,status_code=200)
        else:
            return func.HttpResponse(
                "This HTTP triggered function executed successfully. Pass a valid key in the query string or in the request body for a personalized response.",
                status_code=200
            )
            
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)