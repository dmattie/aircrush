from aircrushcore.Models.Task import Task
from aircrushcore.crushhost.dml.dml_task import TaskRepository
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
        

    
    
    TR=TaskRepository(host=crushHOST)
    
  
    for task in TR.Tasks:
        print(f"{TR.Tasks[task].title}")