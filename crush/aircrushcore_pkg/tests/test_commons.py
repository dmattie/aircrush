import pytest
import os
from os.path import exists
#from aircrushcore.datacommons.models import *
from aircrushcore.datacommons.data_commons import DataCommons
from aircrushcore.controller.configuration import AircrushConfig


dir_path = os.path.dirname(os.path.realpath(__file__))
crush_config=f"{dir_path}/crush.ini"
print(crush_config)
f = open(crush_config,'r')
file_contents = f.read()
aircrush=AircrushConfig(crush_config)
print(aircrush.config['COMMONS']['commons_path'])
dc = DataCommons(aircrush)

def test_configuration():    
        
    assert(len(dc.commons_path)>0)
    
    
def test_initialize():
    
    assert(dc.initialize())

def test_project_collection():
    projects=dc.Projects()
    assert(len(projects)>0)

def test_sync_to_cms():
    print("sync")
    assert(dc.SyncWithCMS())