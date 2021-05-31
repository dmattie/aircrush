from .. import crush
from aircrushcore.Models.Participant import Participant
import traceback

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

