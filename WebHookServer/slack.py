import sys,os
import requests
import json

# hide slack URL
sys.path.append(os.path.join(os.path.dirname(__file__), "config"))
try:
    from slack_config import slackUrl
except ModuleNotFoundError as e:
    print(e)

url = slackUrl

def post_SlackMessage(message):

    payload = {"text" : "ALERT: " + message}
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    if response.status_code != 200:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )