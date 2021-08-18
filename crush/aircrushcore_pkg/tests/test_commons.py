import pytest
from os.path import exists
from aircrushcore.datacommons.models import *
from aircrushcore.controller.configuration import AircrushConfig



crush_config='crush.ini'
config=AircrushConfig(crush_config)
dc = DataCommons(config)

def test_configuration():    
        
    assert(len(dc.commons_path)>0)
    assert(dc.staging_path=='/media/dmattie/GENERAL/aircrush_data_commons/.aircrush')
    
def test_initialize():
    
    assert(dc.initialize())

def test_project_collection():
    projects=dc.Projects()
    assert(len(projects)>0)
