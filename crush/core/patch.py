import sys
import requests
import json
import configparser
from authentication import crushConnection

cc=crushConnection()
session=cc.getConnectionToken()


head = {"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json","X-CSRF-Token":cc.csrf_token}
url = f'http://localhost:81/jsonapi/node/exam/a3df768d-0b80-4122-a289-1336bcb25bda'
payload = {"data" : {
    "type":"node--exam",
    "id":"a3df768d-0b80-4122-a289-1336bcb25bda",
    "attributes":{
        "field_directory_format":"unknown",
        "title":"dave"
    }
}}

#payload='{"data": {"type": "node--exam", "id": "a3df768d-0b80-4122-a289-1336bcb25bda", "attributes": {"field_directory_format": "unknown", "title":"dave"}}}'


r = session.patch(url, json.dumps(payload), headers=head)
#print(r.request.body)
#print(r.request.headers)
#print(r.request.url)
print(r.status_code)
print(r.reason)
#print(r.json())