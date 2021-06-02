#from aircrushcore.Models.Task import Task
#from aircrushcore.Models.Project import Project
#from aircrushcore.Models.Participant import Project
import aircrushcore.Models

from aircrushcore.crushhost.dml.dml_task import TaskRepository
from aircrushcore.crushhost.dml.dml_project import ProjectRepository
from aircrushcore.crushhost.dml.dml_participant import ParticipantRepository
from aircrushcore.crushhost.dml.dml_session import SessionRepository

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
    
    for project in PROJREPO.Projects:
        print(f"{PROJREPO.Projects[project].title}")
        PARTREPO= ParticipantRepository(host=crushHOST,project=project)
        for participant in PARTREPO.Participants:
            print(f"\t{PARTREPO.Participants[participant].title}")
            SESSREPO= SessionRepository(host=crushHOST,project=project)
            for session in SESSREPO.Sessions:
                print(f"\t\t{SESSREPO.Sessions[session].title}")
                for task in TR.Tasks:
                    print(f"\t\t\t{TR.Tasks[task].title}, prereqs:{TR.Tasks[task].field_prerequisite_tasks}")