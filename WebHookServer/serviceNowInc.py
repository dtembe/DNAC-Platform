import sys,os
import requests
import json
import urllib3
from requests.auth import HTTPBasicAuth

#SSL Warnings Disabled when uncommented. Comment out to turn on SSL Warnings.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# hide the sn user/pass token
sys.path.append(os.path.join(os.path.dirname(__file__), "config"))
try:
    from sn_config import snowemuser, snowempassword, snowurlincident
except ModuleNotFoundError as e:
    print(e)

url = snowurlincident

def open_incident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, header, message):
#def open_incident(message, header):
    try:
        #jsonarray = l
        o_caller = ("Event Management")
        o_category = ("Network")
        o_subcategory = ("Internal Application")
        o_business_service = ("IT Services")
        o_configuration_item = ("")
        o_contact_type = ("Alert")
        o_state = ("New")
        o_impact = ('3')  #this works
        o_urgency = ('1')
        o_assignment_group = ("Network")
        o_assigned_to = ("")
        o_short_description = (header)
        o_description = (message)
        print ("-" * 50)
        print (o_caller, o_category, o_subcategory, o_business_service, o_configuration_item, o_contact_type, o_state, o_impact, o_urgency, o_assignment_group, o_assigned_to, o_short_description, o_description )
        print ("-" * 50)
        data = {"caller_id": o_caller, "category": o_category, "subcategory": o_subcategory, "business_service": o_business_service, "cmdb_ci": o_configuration_item, "contact_type": o_contact_type, "state": o_state, "impact": o_impact, "urgency": o_urgency, "assignment_group": o_assignment_group, "assigned_to": o_assigned_to, "short_description": o_short_description, "description": o_description}
        postData = json.dumps(data)
        print(postData)

        try:
            url = snowurlincident
            auth = HTTPBasicAuth(snowemuser, snowempassword)
            head = {'Content-type': 'application/json',
                    'Accept': 'application/json'}
            payld = postData
            ret = requests.post(url, auth=auth, data=payld, headers=head)
            # sys.stdout.write(ret.text)
            returned_data = ret.json()
            #logger.info(returned_data)
            print(returned_data)
        except IOError as e:
            print(e)
            #logger.error(e)
            pass
    except IOError as e:
        print(e)
        #logger.error(e)
        pass

