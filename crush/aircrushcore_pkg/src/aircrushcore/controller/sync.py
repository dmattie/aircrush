from aircrushcore.cms.models.project import Project
from aircrushcore.cms.models.project_collection import ProjectCollection
from aircrushcore.cms.models.session_collection import SessionCollection
from aircrushcore.cms.models.subject_collection import SubjectCollection
from aircrushcore.cms.models.subject import Subject
from aircrushcore.cms.models.session import Session
from aircrushcore.datacommons.models.data_commons import DataCommons
from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.cms.models.host import Host
import asyncio, asyncssh, sys
import traceback
import requests
import json

class Sync():
    def __init__(self,aircrush:AircrushConfig):
        self.aircrush=aircrush 

        self.crush_host=Host(
            endpoint=aircrush.config['REST']['endpoint'],
            username=aircrush.config['REST']['username'],
            password=aircrush.config['REST']['password']
            )       

    def sync_projects(self):
        dc=DataCommons(self.aircrush)

   
    async def _run_project_status_client(self,host:str,username:str,password:str,cmd:str,uuid:str,crushHOST:Host):
    

        async with asyncssh.connect(host,username=username, password=password, known_hosts=None) as conn:
            agentresult = await conn.run(cmd, check=True)
            
            project=uuid
            
            subject_collection=SubjectCollection(cms_host=crushHOST,project=uuid)
            session_collection=SessionCollection(cms_host=crushHOST,project=uuid)

            subjects=subject_collection.get()
            
            try:
                agentExams=json.loads(agentresult.stdout)
            except:                
                traceback.print_exc()                
                raise Exception("ERROR:sync_participant::Agent didn't return JSON")
            
            newnodes=0
            updatednodes=0

            #Iterate exams in Project Directory
            for participant in agentExams['participants']: 

                isbids="unknown"           
                subject_metadata={
                        "title":agentExams['participants'][participant]['id'],
                        "isbids":isbids,
                        "field_project":project,
                        "uuid":None,
                        "cms_host":self.crush_host            
                    }                
                
                #Look for existing subject
                for subject_guid in subjects:
                    subject=subjects[subject_guid]                    
                    if participant==subject.title:                                          
                        subject_metadata['uuid']=subject.uuid                        
                #Upsert regardless
                s = Subject(metadata=subject_metadata)
                participant_uuid=s.upsert()                    
                                
                #Upsert any associated sessions--------------------------------
                
                sessions=session_collection.get(subject=subject.uuid)
                
            
                for data_commons_sessions in agentExams['participants'][participant]['sessions']:                            
                    
                    session_metadata={
                            "title":data_commons_sessions,
                            "field_participant":participant_uuid,
                            "field_status":"notstarted",    
                            "uuid":None,                                
                            "cms_host":self.crush_host
                        }  
                    sessionExists=False

                    #Look for existing session
                    for cms_session_guid in sessions:
                        cms_session=sessions[cms_session_guid]
                        if data_commons_sessions==cms_session.title:                            
                            session_metadata['uuid']=cms_session.uuid

                    s = Session(metadata=session_metadata)                    
                    s.upsert()     

                #Unpublish any sessions not found
                for session_guid in sessions:
                    if sessions[session_guid].title not in agentExams['participants'][participant]['sessions']:
                        sessions[session_guid].published=False
                        sessions[session_guid].upsert()

            #Unpublish any subjects not found
            for subject_guid in subjects:
                if subjects[subject_guid].title not in agentExams['participants']:
                    subjects[subject_guid].published=False
                    subjects[subject_guid].upsert()

    
    def sync_subject_sessions(self):
                  
        dc=DataCommons(self.aircrush)              
        proj_collection=ProjectCollection(cms_host=self.crush_host)  
        project_list=dc.Projects()        
        
        cms_projects = proj_collection.get()
        project=None
        for project_uuid in cms_projects:
            project = proj_collection.get_one(project_uuid)
    
            cmd=f"python3.8 {project.field_path_to_crush_agent}/ps2.py {project.field_path_to_exam_data}"
            print(cmd)
            asyncio.get_event_loop().run_until_complete(
                    self._run_project_status_client(
                        host=project.field_host,
                        username=project.field_username,
                        password=project.field_password,                
                        cmd=cmd,
                        uuid=project.uuid,
                        crushHOST=self.crush_host
                    )
                )  
                                     
                                
