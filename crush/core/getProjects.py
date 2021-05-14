import asyncio, asyncssh, sys
import requests
import json
#import configparser
import crushhost 


#########
#config = configparser.ConfigParser()
#config.read('../crush.ini')

#endpoint=config['REST']['endpoint']
#u=config['REST']['username']
#p=config['REST']['password']

crush=crushhost.crush(
                    endpoint="http://localhost:81/",
                    username="crush",
                    password="crush"
                    )


print(f"Connected to CRUSH Host at {crush.connection.endpoint}")
async def run_project_status_client(host,username,password,cmd,uuid):
   # with open("/home/dmattie/.ssh/id_rsa","r") as mypkey:
   #     keydata=mypkey.readlines()
   # print(keydata)
    async with asyncssh.connect(host,username=username, password=password, known_hosts=None) as conn:
        result = await conn.run(cmd, check=True)
        
        #rExams = requests.get(f'{endpoint}/jsonapi/node/exam', auth=(u, p)) #Get Known Exams from Crush host
        rExams = crush.get('jsonapi/node/exam')

        projectExams=json.loads(result.stdout)
        newnodes=0
        updatednodes=0
        for exam in projectExams: #Iterate exams in Project Directory
            
            if projectExams[exam]['isbids']=="True": 
                isbids="bids"
            else:
                isbids="unknown"
            
            #get other status variables
            #
            # Lets look for a known match on CRUSH HOST
            found=False
            for ex in rExams.json()['data']:  #Iterate exams on CRUSH HOST
                if(ex['type']=='node--exam'): #If this is an EXAM type
                    #print("are we on the right project?  crushhost:%s, uuid:%s" %(ex['relationships']['field_project']['data']['id'],uuid))
                    if (ex['relationships']['field_project']['data']['id']==uuid):  #IF this exam is for the project we are interested in...
                        exuuid=ex['id']
                        exid=ex['attributes']['field_exam_id']
                        exproject=uuid
                        #project=item['attributes']['title']
                        #TODO get collection of exam IDs, UUIDs,project 
                        
                        if exid==exam:  #If we are updating an existing exam on CRUSH HOST 
                            found=True
                                                       
                            #head = {"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json"}
                            url = f'jsonapi/node/exam/{exuuid}'
                            payload = {"data" : {
                                "type":"node--exam",
                                "id":exuuid,
                                "attributes":{
                                    "field_directory_format":isbids,
                                    "title":exid
                                }
                            }}
                            
                            r= crush.patch(url,payload)
                            if(r.status_code!=200):
                                print("[ERROR] failed to update {exid} on CRUSH GUI: {r.status_code},  {r.reason}")
                            else:
                                updatednodes=updatednodes+1                                                       
                            
            if not found:                

                url = f'jsonapi/node/exam'

                if projectExams[exam]['isbids']=="True": 
                    isbids="bids"
                else:
                    isbids="unknown"

                payload = {"data" : {
                    "type":"node--exam",                    
                    "attributes":{
                        "field_directory_format":isbids,
                        "title":projectExams[exam]['id'],
                        "field_exam_id":projectExams[exam]['id']
                    },
                    "relationships": {
                        "field_project": {
                            "data": {
                                "type": "node--project",
                                "id": uuid
                            }
                        }
                        
                    }
                }}
                

                #print(f"Registering {exam} with CRUSH")
                
                r= crush.post(url,payload)
                if(r.status_code!=201):
                    print(f"[ERROR] failed to create {exam} on CRUSH GUI: {r.status_code},  {r.reason}")
                else:
                    newnodes=newnodes+1

        print(f"{newnodes} created, {updatednodes} updated.  The flux core is hot!")                                
                               


r = crush.get('jsonapi/node/project')
#r = requests.get(f'{endpoint}/jsonapi/node/project', auth=(u, p))

if r.status_code==200:  #We can connect to CRUSH host
    # Iterate the projects
    
    if len(r.json()['data'])==0:
        print("No projects defined in CRUSH Host.  Create a project first.")
        exit()
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

            
else:
    print(f"Error connecting to CRUSH Host:{r.status_code}, {r.reason} ")

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