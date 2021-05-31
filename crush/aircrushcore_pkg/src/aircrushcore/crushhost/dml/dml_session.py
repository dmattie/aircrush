from .. import crush
from aircrushcore.Models.Session import Session
from . dml_participant import ParticipantRepository
import traceback

class SessionRepository():
    
    
    def __init__(self,**kwargs):    
        self.Sessions={}    
        self.Project=""
        if "host" in kwargs:
            self.HOST=kwargs['host']           
        else:
            print("\nERROR:SessionRepository::HOST not specified\n")
        
        if "project" in kwargs:
            self.Project=kwargs['project']
            print("Project limited")
        else:
            self.Project=""
            print("Unrestricted")

        ParticipantRepositoryMetadata={
            "host":self.HOST
        }
        if self.Project:
            ParticipantRepositoryMetadata['project']=self.Project
            
        print(f"restricting sessons to {self.Project}")
        PR=ParticipantRepository(host=self.HOST, project=self.Project)
        
        self.KnownParticipants=PR.getKnownParticipants()
        self.Sessions=self.getKnownSessions()
        
            
    def getKnownSessions(self):
        r = self.HOST.get('jsonapi/node/session')
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("SessionRepository:: No sessions found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--session'):
                        #IF this session is within the project specified
                        inScope=False
                        for p in self.KnownParticipants:
                            if self.KnownParticipants[p].uuid==item['relationships']['field_participant']['data']['id']:
                                inScope=True
                                print(f"{p} In scope")
                        if self.Project=="" or inScope:
                            uuid=item['id']

                            metadata={    
                                "title":item['attributes']['title']  ,                            
                                "field_participant":item['relationships']['field_participant']['data']['id'] ,   
                                "field_status":item['attributes']['field_status'],
                                "uuid":uuid                                              
                            }

                            self.Sessions[item['id']]=Session(metadata=metadata)     
            return self.Sessions                   

    def upsertSession(self,session):
        print("Upserting")
        
        for s in self.Sessions:
            print(f"{self.Project} - {s}")
        try:            
            if session.uuid in self.Sessions:                
                print(f"SessionRepository::found session profile for [{session}] [{self.Sessions[session].title}] on CRUSH host, syncing metadata")

                # payload = {
                #     "data" : {
                #         "type":"node--participant",    
                #         "id":self.Participants[participant].uuid,                
                #         "attributes":{
                #             "title": participant.title,                                                    
                #             "field_status": participant.field_status,
                #         },
                #         "relationships":{
                #             "field_project":{
                #                 "data":{
                #                     "type":"node--project",
                #                     "id":participant.field_project
                #                 }
                #             }                         
                #         }              
                #     }
                # }

                               
                
                # r= self.HOST.patch(f"jsonapi/node/participant/{self.Participants[participant].uuid}",payload)
                # if(r.status_code!=200):                   
                #     print(f"[ERROR] failed to patch participant {participant.uuid} ({particpant.title}) on CRUSH HOST: {r.status_code},  {r.reason}")
                # else:                    
                #     if len(r.json()['data'])==0:
                #         print("ParticipantRepository::UpsertParticipant:  Participant not updated.")                
                #     else:       
                #         return r.json()['data']['id']
                    
                # #Update
            else:
                print(f"SessionRepository::New {session.title}, Inserting")
                #Insert

                
                payload = {
                    "data" : {
                        "type":"node--session",                                           
                        "attributes":{
                            "title": session.title,                                                    
                            "field_status": session.field_status,
                        },
                        "relationships":{
                            "field_participant":{
                                "data":{
                                    "type":"node--participant",
                                    "id":session.field_participant
                                }
                            }                         
                        }              
                    }
                }

               # print(payload)                

                r= self.HOST.post("jsonapi/node/session",payload)
                if(r.status_code!=201):                   
                    print(f"[ERROR] failed to create session {session.title} on CRUSH HOST: {r.status_code},  {r.reason}")
                else:
                    
                    if len(r.json()['data'])==0:
                        print("SessionRepository::UpsertSession:  Session not created.")                
                    else:       
                        return r.json()['data']['id']
                    

        except:
            if( not isinstance(session,Session)):
                print("Session object not passed to upsert")
            else:
                 traceback.print_exc()

