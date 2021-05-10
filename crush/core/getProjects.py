import asyncio, asyncssh, sys
import requests
import json
import configparser

#########
config = configparser.ConfigParser()
config.read('../crush.ini')

endpoint=config['REST']['endpoint']
u=config['REST']['username']
p=config['REST']['password']

r = requests.get(f'{endpoint}/jsonapi/node/project', auth=(u, p))

async def run_project_status_client(host,username,password,cmd,uuid):
   # with open("/home/dmattie/.ssh/id_rsa","r") as mypkey:
   #     keydata=mypkey.readlines()
   # print(keydata)
    async with asyncssh.connect(host,username=username, password=password, known_hosts=None) as conn:
        result = await conn.run(cmd, check=True)
        
        rExams = requests.get(f'{endpoint}/jsonapi/node/exam', auth=(u, p)) #Get Known Exams from Crush host
        
        
        projectExams=json.loads(result.stdout)

        for exam in projectExams: #Iterate exams in Project Directory
            
            if projectExams[exam]['isbids']=="True": 
                isbids="bids"
            else:
                isbids="unknown"
            
            #get other status variables

            for ex in rExams.json()['data']:  #Iterate exams on CRUSH HOST
                if(ex['type']=='node--exam'): #If this is an EXAM type
                    if (ex['relationships']['field_project']['data']['id']==uuid):  #IF this exam is for the project we are interested in...
                        exuuid=ex['id']
                        exid=ex['attributes']['field_exam_id']
                        exproject=uuid
                        #project=item['attributes']['title']
                        #TODO get collection of exam IDs, UUIDs,project 
                        
                        if exid==exam:  #If we are updating an existing exam on CRUSH HOST                            
                            head = {"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json"}
                            url = f'{endpoint}/jsonapi/node/exam/{exuuid}'
                            payload = {"data" : {
                                "type":"node--exam",
                                "id":exuuid,
                                "attributes":{
                                    "field_directory_format":isbids,
                                    "title":"dave"
                                }
                            }}
                            print(payload)
                            #r = requests.Request('PATCH',url, payload, headers=head,auth=(u, p))
                            r = requests.patch(url, payload, headers=head,auth=(u, p))
                            print(r.request.body)
                            print(r.request.headers)
                            print(r.request.url)
                            print(r.status_code)
                            print(r.reason)
                            print(r.json())
                            #prepared=r.prepare()
                            #pretty_print_REST(prepared)
                            #s=requests.Session()
                            #s.send(prepared)
                            

                        else: #We are creating a new exam on CRUSH HOST
                            pass
                            #Create exam on crushhost



# Iterate the projects
for item in r.json()['data']:
    if(item['type']=='node--project'):
        uuid=item['id']
        project=item['attributes']['title']
        host=item['attributes']['field_host']
        username=item['attributes']['field_username']
        password=item['attributes']['field_password']
        agentpath=item['attributes']['field_path_to_crush_agent']
        examPath=item['attributes']['field_path_to_exam_data']
        print(f'Connecting to {project:20s}')
        try:
            cmd='python ' + agentpath + '/project_status.py ' + examPath
            print(cmd)
            asyncio.get_event_loop().run_until_complete(run_project_status_client(
                host=host,
                username=username,
                password=password,                
                cmd=cmd,
                uuid=uuid
            ))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))


# client_key = asyncssh.read_private_key(RSA_KEY)

#     async with asyncssh.connect(
#         client_factory=None,
#         host=SERVER_HOST,
#         username=SERVER_USERNAME,
#         port=SERVER_PORT,
#         client_keys=[client_key]
#     ) as conn:
#         res = await conn.run('df')
#         print(res.stdout)


#print(SERVER_HOST)
#async with asyncssh.connect(client_factory=None,host=SERVER_HOST,username=SERVER_USERNAME,client_keys=None) as conn:
#    res = await conn.run('df')
 #   print(res.stdout)