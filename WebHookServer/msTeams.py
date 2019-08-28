import sys,os
import requests
import json

# hide slack URL
sys.path.append(os.path.join(os.path.dirname(__file__), "config"))
try:
    from msTeams_config import msTeamsUrl
except ModuleNotFoundError as e:
    print(e)

url = msTeamsUrl

def post_msTeamsMessage(header, message):

    payload = {
      "@context": "http://schema.org/extensions",
      "@type": "MessageCard",
      "summary": header,
      "sections": [
        {
          "activityTitle": "**Message from Cisco DNA Center **",
          "activitySubtitle": "DNAC",
          "activityText": message
        }
      ]
    }
    headers = {
    'content-type': "application/json"
    }
    response = requests.request("POST", url, data=json.dumps(payload), headers=headers)

    if response.status_code != 200:
        raise ValueError(
            'Request to Microsoft Teams returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)


        )
