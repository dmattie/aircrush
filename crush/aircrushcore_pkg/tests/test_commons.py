import pytest
import os
from os.path import exists
#from aircrushcore.datacommons.models import *
from aircrushcore.datacommons.data_commons import DataCommons
from aircrushcore.controller.configuration import AircrushConfig



#crush_config='crush.ini'
homedir=os.path.expanduser('~')
crush_config=f"{homedir}/.crush.ini"
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