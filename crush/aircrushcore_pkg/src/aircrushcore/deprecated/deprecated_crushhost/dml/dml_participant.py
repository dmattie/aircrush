from .. import crush
from aircrushcore.Models.Participant import Participant
import traceback
import uuid
import asyncio, asyncssh, sys
class ParticipantRepository():
    
    
    def __init__(self,**kwargs):    
        self.Participants={}    
        self.Project=""
    

        if "host" in kwargs:
            self.HOST=kwargs['host']
            
        else:
            raise Exception("\nERROR:ParticipantRepository::HOST not specified\n")

        if "project" in kwargs:
            self.Project=kwargs['project']
    
        self.getKnownParticipants()
    


            
    def getKnownParticipants(self):
        r = self.HOST.get('jsonapi/node/participant')
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("ParticipantRepository:: No participants found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--participant'):
                        if self.Project=="" or self.Project==item['relationships']['field_project']['data']['id']:
                            uuid=item['id']

                            metadata={    
                                "title":item['attributes']['title']  ,                            
                                "field_project":item['relationships']['field_project']['data']['id'] ,   
                                "field_status":item['attributes']['field_status'],
                                "uuid":uuid                                              
                            }

                            self.Participants[item['id']]=Participant(metadata=metadata)     
            return self.Participants                   

    def getOne(self,participant):
        
        ReturnDict={}

        r = self.HOST.get('jsonapi/node/participant')
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("ParticipantRepository:: No participants found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--participant'):
                        if item['id']==participant:
                            if self.Project=="" or self.Project==item['relationships']['field_project']['data']['id']:
                                uuid=item['id']

                                metadata={    
                                    "title":item['attributes']['title']  ,                            
                                    "field_project":item['relationships']['field_project']['data']['id'] ,   
                                    "field_status":item['attributes']['field_status'],
                                    "uuid":uuid                                              
                                }

                                ReturnDict[item['id']]=Participant(metadata=metadata)     
            return ReturnDict                   

    def assignWorker(self,project,subject,worker):
        print(f"{project.title}[{subject.title}] pipelines to be performed on node {worker}")
        
        tar_uid=self.gzSubject(project,subject)

        print(tar_uid)
        source=f"{project.username}@{project.host}"

    def gzSubject(self,project,subject):
        uid=uuid.uuid4()
        cmd=f"mkdir -p {project.field_path_to_exam_data}/.aircrush;tar -czf {project.field_path_to_exam_data}/.aircrush/{uid}__sub-{subject.title}.tar.gz {project.field_path_to_exam_data}/sub-{subject.title}"
        print(cmd)
        asyncio.get_event_loop().run_until_complete(self.gzSubjectWorker(
            host=project.field_host,
            username=project.field_username,
            password=project.field_password,                
            cmd=cmd            
        ))
        
        return uid

 #   async def scp_client(self,source,dest):
#        await asyncssh.scp(source,dest)


    async def gzSubjectWorker(self,host,username,password,cmd):
        
        async with asyncssh.connect(host=host,username=username, password=password, known_hosts=None) as conn:
            agentresult = await conn.run(cmd, check=True)            
            print(agentresult)            
                                
        pass

    def upsertParticipant(self,participant):
        
        try:            
            if participant.uuid:# in self.Participants:                
                print(f"ParticipantRepository::found participant profile for [{participant.title}] [{self.Participants[participant.uuid].title}] on CRUSH host, syncing metadata")

                payload = {
                    "data" : {
                        "type":"node--participant",    
                        "id":participant.uuid,#self.Participants[participant].uuid,                
                        "attributes":{
                            "title": participant.title,                                                    
                            "field_status": participant.field_status,
                        },
                        "relationships":{
                            "field_project":{
                                "data":{
                                    "type":"node--project",
                                    "id":participant.field_project
                                }
                            }                         
                        }              
                    }
                }

                               
                
                r= self.HOST.patch(f"jsonapi/node/participant/{participant.uuid}",payload)
                if(r.status_code!=200):                   
                    print(f"[ERROR] failed to patch participant {participant.uuid} ({particpant.title}) on CRUSH HOST: {r.status_code},  {r.reason}")
                else:                    
                    if len(r.json()['data'])==0:
                        print("ParticipantRepository::UpsertParticipant:  Participant not updated.")                
                    else:       
                        return r.json()['data']['id']
                    
                #Update
            else:
                print(f"ParticipantRepository::New {participant.title}, Inserting")
                #Insert

                
                payload = {
                    "data" : {
                        "type":"node--participant",                                           
                        "attributes":{
                            "title": participant.title,                                                    
                            "field_status": participant.field_status,
                        },
                        "relationships":{
                            "field_project":{
                                "data":{
                                    "type":"node--project",
                                    "id":participant.field_project
                                }
                            }                         
                        }              
                    }
                }

               # print(payload)                

                r= self.HOST.post("jsonapi/node/participant",payload)
                if(r.status_code!=201):                   
                    print(f"[ERROR] failed to create participant {participant.title} on CRUSH HOST: {r.status_code},  {r.reason}")
                else:
                    print(r.json())
                    if len(r.json()['data'])==0:
                        print("ParticipantRepository::UpsertParticipant:  Participant not created.")                
                    else:       
                        return r.json()['data']['id']
                    

        except:
            if( not isinstance(participant,Participant)):
                print("Participant object not passed to upsert")
            else:
                 traceback.print_exc()

