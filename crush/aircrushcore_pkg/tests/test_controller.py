import pytest

from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.controller.sync import Sync
from aircrushcore.datacommons.models.data_commons import DataCommons
from aircrushcore.cms.models.project_collection import ProjectCollection
from aircrushcore.cms.models.project import Project
from aircrushcore.cms.models.host import Host



crush_config='crush.ini'
aircrush=AircrushConfig(crush_config)

crush_host=Host(
    endpoint=aircrush.config['REST']['endpoint'],
    username=aircrush.config['REST']['username'],
    password=aircrush.config['REST']['password']
    )

def test_sync_projects():

    sync=Sync(aircrush)
    dc=DataCommons(aircrush)

    project_list=dc.Projects()

    sync.sync_projects()

    proj_collection=ProjectCollection(cms_host=crush_host)
     
    cms_projects = proj_collection.get()

    assert(len(project_list)>0)
    assert(len(cms_projects)>=len(project_list)) #There may be more manually deposited
    

def test_sync_subjects():
    sync=Sync(aircrush)
   # dc=DataCommons(aircrush)

    #project_list=dc.Projects()

    sync.sync_subject_sessions()

    #proj_collection=ProjectCollection(cms_host=crush_host)
     
    #cms_projects = proj_collection.get()

    #assert(len(project_list)>0)
    #assert(len(cms_projects)>=len(project_list)) #There may be more manually deposited

    assert(False)
