import crushhost 

crush=crushhost.crush(
                    endpoint="http://localhost:81/",
                    username="crush",
                    password="crush"
                    )


print (crush.connection.endpoint)


url = f'jsonapi/node/exam/a3df768d-0b80-4122-a289-1336bcb25bda'
payload = {"data" : {
    "type":"node--exam",
    "id":"a3df768d-0b80-4122-a289-1336bcb25bda",
    "attributes":{
        "field_directory_format":"unknown",
        "title":"dave"
    }
}}

crush.patch(url,payload)
