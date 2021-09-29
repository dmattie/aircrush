#from aircrushcore.Models.Task import Task
#from aircrushcore.Models.Project import Project
#from aircrushcore.Models.Participant import Project
import aircrushcore.Models
from aircrushcore.Models.TaskInstance import TaskInstance
from aircrushcore.crushhost.dml.dml_task import TaskRepository
from aircrushcore.crushhost.dml.dml_project import ProjectRepository
from aircrushcore.crushhost.dml.dml_participant import ParticipantRepository
from aircrushcore.crushhost.dml.dml_session import SessionRepository
from aircrushcore.crushhost.dml.dml_task_instance import TaskInstanceRepository
from aircrushcore.crushhost.crush import crush
import asyncio, asyncssh, sys
import requests
import json

import importlib
import traceback

def sync(host):
        
    crushHOST=None

    try:
        crushHOST=crush(
            endpoint="http://localhost:81/",
            username="crush",
            password="crush"
            )
    except:
        raise Exception("ERROR: Unable to connect to crush host")
        

    
    
    PROJREPO = ProjectRepository(host=crushHOST)
    TR=TaskRepository(host=crushHOST)
    TIREPO = TaskInstanceRepository(host=crushHOST)
    
    for project in PROJREPO.Projects:
        print(f"{PROJREPO.Projects[project].title}")
        print(f"Number of active pipelines: {len(PROJREPO.Projects[project].field_activated_pipelines)}")
        PARTREPO= ParticipantRepository(host=crushHOST,project=project)
        for pipeline in PROJREPO.Projects[project].field_activated_pipelines:
            print(f"Processing pipeline:{pipeline}")
            for participant in PARTREPO.Participants:
                print(f"\t{PARTREPO.Participants[participant].title}")
                SESSREPO= SessionRepository(host=crushHOST,project=project,participant=participant)
                for session in SESSREPO.Sessions:
                    print(f"\t\t{SESSREPO.Sessions[session].title}")
                    for task in TR.Tasks:
                        if TR.Tasks[task].field_pipeline in PROJREPO.Projects[project].field_activated_pipelines:
                            print(f"\t\t\t{TR.Tasks[task].title}",
                            f"\n\t\t\t\tprereqs:{TR.Tasks[task].field_prerequisite_tasks}",
                            f"\n\t\t\t\tfield_pipeline:{TR.Tasks[task].field_pipeline}",
                            f"\n\t\t\t\tfield_id:{TR.Tasks[task].field_id}",
                            f"\n\t\t\t\tfield_parameters:{TR.Tasks[task].field_parameters}"                        
                            )

                            TI = TIREPO.get(session=session,task=task)
                            if len(TI)==0:
                                metadata={
                                    "title":TR.Tasks[task].title,
                                    "field_associated_participant_ses":SESSREPO.Sessions[session].uuid,
                                    "field_pipeline":TR.Tasks[task].field_pipeline,
                                    "field_task":TR.Tasks[task].field_id,

                                }
                                print("NEW--------------------------------------------------------------")
                                print(metadata)
                                TIREPO.upsert(TaskInstance(metadata=metadata))
                        
                            else:
                                for T in TI:                        
                                    print(f"Task Instance(s) found matching session/task: {TI[T].title}")


                        