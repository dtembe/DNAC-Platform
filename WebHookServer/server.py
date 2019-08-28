#!/usr/bin/env python
from __future__ import print_function
from flask import Flask
from flask import request
app = Flask(__name__)


#from gmail import send_mail
from webex_teams import post_message
from serviceNowInc import open_incident
from slack import post_SlackMessage
from msTeams import post_msTeamsMessage

def old_format_event(event):

    header = 'Event:{}, Severity:{}, Category:{}\n'.format(event['title'],
                                                      event['severity'],
                                                      event['category'])
    message = '{}\n'.format(event['description'])

    message += "\nSuggested Actions:\n"
    if event['title'] == "Device Image Outdated":
        device = event['enrichmentInfo']['connectedDevice'][0]['deviceDetails']
        image = event['enrichmentInfo']['imageDetails']['goldenImage']['imageVersion']
        message += "Update device {}[{}] running {} to {}\n".format(device['hostname'],
                                                             device['managementIpAddress'],
                                                             device['softwareVersion'],
                                                             image)
    else:
        for action in event['enrichmentInfo']['issueDetails']['issue'][0]['suggestedActions']:
            message += " -{}\n".format(action['message'])

    caller = "Event Management"
    categoryList = "Network"
    subcategoryList = "Internal Application"
    businessServiceLookup = "IT Services"
    cmdb_ciLookup = ""
    contact_typeList = "Alert"
    stateList = "New"
    impact = "3"
    urgency = "1"
    assignmentGroupLookup = "Network"
    assigned_toLookup = ""

    return caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, header, message

def new_format_event(dnac,event):
    header = 'Event:{}, Category:{}\n'.format(event['eventId'], event['category'])
    message = '\n'.join([ '{}:{}'.format(k,v) for k,v in event['details'].items()])
    if 'ciscoDnaEventLink' in event:
        message += "\nEventURL: https://{}/{}".format(dnac,event['ciscoDnaEventLink'])
    caller = "Event Management"
    categoryList = "Network"
    subcategoryList = "Internal Application"
    businessServiceLookup = "IT Services"
    cmdb_ciLookup = ""
    contact_typeList = "Alert"
    stateList = "New"
    impact = "3"
    urgency = "1"
    assignmentGroupLookup = "Network"
    assigned_toLookup = ""

    return caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, header, message

def format_event(dnac,event):
    if 'title' in event:
        return(old_format_event(event))
    else:
        return (new_format_event(dnac,event))

def handle(dnac, event):
    '''
    handles an event.  Can send an email, or message to webex.
    :param event:
    :return:
    '''
    caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, header, message = format_event(dnac, event)
    print(message)

    # send to webex
    post_message("*******\n" + header + message)

    # send an email
    #send_mail(header,message)


    #send to ServiceNow Incident
    open_incident(caller, categoryList, subcategoryList, businessServiceLookup, cmdb_ciLookup, contact_typeList, stateList, impact, urgency, assignmentGroupLookup, assigned_toLookup, header, message)

    #Send to Slack URL
    post_SlackMessage("*******\n" + header + message)

    #Send to MS Teams as a Notification
    post_msTeamsMessage(header, message)

@app.route('/', defaults={'path': ''}, methods=['GET','POST'])
@app.route('/<path:path>', methods=["GET","PUT","POST","DELETE"])

def get_all(path):
    print("Method {}, URI {}".format(request.method,path))
    if request.method == "POST":
        print (request.headers)
        print (request.json)
        if request.json != {}:
            handle(request.remote_addr, request.json)
        else:
            print("skipping - empty")
    return ("OK")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="9000", ssl_context='adhoc')
