import pytest
from aircrushcore.cms.models import *
import random
import uuid

import configparser


config = configparser.ConfigParser()
config.read('crush.ini')

crush_host=Host(
    endpoint=config['REST']['endpoint'],
    username=config['REST']['username'],
    password=config['REST']['password']
    )
 
   
def create_sample_project():
    metadata={    
            "title":"UAT Test for test_guids"  ,                            
            "field_host":"test host" ,   
            "field_password":"test password",
            "field_path_to_crush_agent":"test path to crush agent",
            "field_path_to_exam_data":"test path to exam data",
            "field_username":"test username",
            "body":"This is a test project created by automated unit testing",  
            "cms_host":crush_host              
        }

    p = Project(metadata=metadata)    
    puid = p.upsert()
    return puid
def create_sample_subject(puid:str):
    subject_metadata={
        "title":"ATEST01",
        "field_project":puid,
        "cms_host":crush_host        
    }    
    s = Subject(metadata=subject_metadata)
    suid = s.upsert()
    return suid

def create_sample_session(suid:str):
    metadata={
        "title":"SES-01",
        "field_participant":suid,
        "field_status":"notstarted",
        "cms_host":crush_host
    }
    s = Session(metadata=metadata)
    session_uuid = s.upsert()
    return session_uuid

def create_sample_pipeline():
    title=f"automated-test-pipeline {uuid.uuid4()}"
    metadata={
        "title":title,
        "field_author":"pytest",
        "field_author_email":"nobody@nowhere.com",
        "body":"Lorem ipsum",
        "field_id":"automated_test_pipeline",
        "field_plugin_warnings":"no warnings",
        "cms_host":crush_host
    }
    p = Pipeline(metadata=metadata)
    puid=p.upsert()
    return puid

def create_sample_task(puid:str):
    metadata={
        "title":"automated-test-task-01",
        "field_id":"automated_test_task_01",
        "field_parameters":"a=b,c=d",
        "field_operator":"test_operator",
        "field_prerequisite_tasks":[],
        "cms_host":crush_host,
        "field_pipeline":puid
    }
    t = Task(metadata=metadata)
    tuid=t.upsert()
    return tuid
def create_sample_task_instance(session_uid:str,pipeline_uid:str,task_uid:str):
    metadata={
        "title":"automated-test-task-instance-aa",
        "field_associated_participant_ses":session_uid,
        "field_pipeline":pipeline_uid,
        "body":"Body of test task instance aa",
        "field_remainint_retries":5,
        "field_status":"notstarted",
        "field_task":task_uid,
        "cms_host":crush_host  
    }
    ti = TaskInstance(metadata=metadata)
    ti_uid=ti.upsert()
    return ti_uid

def test_login():
    
    assert crush_host != None
    assert crush_host.username=="crush"
    assert crush_host.session!=None

def test_get_project():
    #Create test project, get it, then delete it
    proj_collection=ProjectCollection(cms_host=crush_host)
    puid=create_sample_project()  
    p = proj_collection.get_one(uuid=puid)
    assert(p.title=="UAT Test for test_guids") 
    p.delete()

def test_get_subject():
    puid=create_sample_project()
    suid = create_sample_subject(puid=puid)
    proj_collection=ProjectCollection(cms_host=crush_host)
    subj_collection=SubjectCollection(cms_host=crush_host)

    s = subj_collection.get_one(uuid=suid)

    assert(s.title=="ATEST01")
    assert(isinstance(s,Subject)==True)
    assert(s.delete()==True)
    
    p = proj_collection.get_one(uuid=puid)
    p.delete()

def test_get_session():
    puid=create_sample_project()
    suid = create_sample_subject(puid=puid)
    sessuid = create_sample_session(suid=suid)

    proj_collection=ProjectCollection(cms_host=crush_host)
    subj_collection=SubjectCollection(cms_host=crush_host)
    sess_collection=SessionCollection(cms_host=crush_host)

    s = sess_collection.get_one(uuid=sessuid)

    assert(s.title=="SES-01")
    assert(isinstance(s,Session)==True)
    assert(s.delete()==True)
    
    subj = subj_collection.get_one(uuid=suid)
    subj.delete()

    p = proj_collection.get_one(uuid=puid)
    p.delete()


def test_get_pipeline():
    puid=create_sample_pipeline()
    pipe_collection=PipelineCollection(cms_host=crush_host)
    p=pipe_collection.get_one(uuid=puid)
    #assert(p.title=="automated-test-pipeline")
    assert(p.field_author=="pytest")
    assert(p.field_author_email=="nobody@nowhere.com")
    #assert(p.body.value=="Lorem ipsum")
    assert(p.field_id=="automated_test_pipeline")
    assert(p.field_plugin_warnings=="no warnings")
    p.delete()

def test_get_task():
    puid=create_sample_pipeline()
    pipe_collection=PipelineCollection(cms_host=crush_host)
    p=pipe_collection.get_one(uuid=puid)

    tuid=create_sample_task(puid)

    task_collection=TaskCollection(cms_host=crush_host)
    t = task_collection.get_one(uuid=tuid)
    assert(t.title=='automated-test-task-01')
    assert(t.field_id=="automated_test_task_01")
    assert(t.field_parameters=="a=b,c=d")
    assert(t.field_operator=="test_operator")
    
    t.delete()
    p.delete()

def test_get_task_instance():
    project_uid=create_sample_project()
    subject_uid = create_sample_subject(puid=project_uid)
    session_uid = create_sample_session(suid=subject_uid)
    pipeline_uid=create_sample_pipeline()
    task_uid=create_sample_task(pipeline_uid)

    task_instance_uid = create_sample_task_instance(session_uid,pipeline_uid,task_uid)

    proj_collection=ProjectCollection(cms_host=crush_host)
    subj_collection=SubjectCollection(cms_host=crush_host)
    sess_collection=SessionCollection(cms_host=crush_host)
    pipe_collection=PipelineCollection(cms_host=crush_host)
    task_collection=TaskCollection(cms_host=crush_host)
    task_instance_collection=TaskInstanceCollection(cms_host=crush_host)

    ti = task_instance_collection.get_one(uuid=task_instance_uid)

    assert(ti.title=="automated-test-task-instance-aa")
    assert(isinstance(ti,TaskInstance)==True)
    assert(ti.delete()==True)
    
    task = task_collection.get_one(uuid=task_uid)
    pipe = pipe_collection.get_one(uuid=pipeline_uid)
    sess = sess_collection.get_one(uuid=session_uid)
    subj = subj_collection.get_one(uuid=subject_uid)
    proj = proj_collection.get_one(uuid=project_uid)

    task.delete()
    pipe.delete()
    sess.delete()    
    subj.delete()
    proj.delete()

    