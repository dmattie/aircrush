import pytest

from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.controller.sync import Sync
from aircrushcore.datacommons.models.data_commons import DataCommons
from aircrushcore.cms.project_collection import ProjectCollection
from aircrushcore.cms.subject_collection import SubjectCollection
from aircrushcore.cms.project import Project
from aircrushcore.cms.host import Host



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
    dc=DataCommons(aircrush)        
    sync.sync_subject_sessions()
    cms_project_collection = ProjectCollection(cms_host=crush_host)
    dc_project_list=dc.Projects()

    for dc_project in dc_project_list:
        
        dc_subjects = dc.Subjects(dc_project)
        project = cms_project_collection.get_one_by_name(dc_project)
        if project:            
            cms_subjects=SubjectCollection(cms_host=crush_host, project=project.uuid)
            assert(len(dc_subjects)==len(cms_subjects))

    #proj_collection=ProjectCollection(cms_host=crush_host)
     
    #cms_projects = proj_collection.get()

    #assert(len(project_list)>0)
    #assert(len(cms_projects)>=len(project_list)) #There may be more manually deposited

    #assert(False)
