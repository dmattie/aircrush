import pytest
from aircrushcore.cms.models import *
import random

import configparser
from .cms_setup import *


def test_login():
    
    assert crush_host != None
    assert crush_host.username=="crush"
    assert crush_host.session!=None

def test_get_project():
    #Create test project, get it, then delete it
    proj_collection=ProjectCollection(cms_host=crush_host)
    puid1=create_sample_project()  
    puid2=create_sample_project()  
    p1 = proj_collection.get_one(uuid=puid1)
    assert(p1.title=="UAT Test for test_guids") 
    

    multiple_projects = proj_collection.get()
    assert(len(multiple_projects)>=2)
    
    p1.delete()
    p2 = proj_collection.get_one(uuid=puid2)    
    p2.delete()


def test_get_project_by_name():
    #Create test project, get it, then delete it
    proj_collection=ProjectCollection(cms_host=crush_host)
    puid1=create_sample_project()  
     
    p1 = proj_collection.get_one_by_name(project_name="UAT Test for test_guids")
    assert(p1.title=="UAT Test for test_guids") 
    
    p1.delete()    

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
    
    #assert(len(s.active_pipelines())>0)
    assert(s.delete()==True)
    
    subj = subj_collection.get_one(uuid=suid)
    subj.delete()

    p = proj_collection.get_one(uuid=puid)
    p.delete()

def test_update_session():
    puid=create_sample_project()
    suid = create_sample_subject(puid=puid)
    sessuid = create_sample_session(suid=suid)
    print(f"===================SAMPLE CREATED {sessuid}==========================")

    proj_collection=ProjectCollection(cms_host=crush_host)
    subj_collection=SubjectCollection(cms_host=crush_host)
    sess_collection=SessionCollection(cms_host=crush_host)

    s = sess_collection.get_one(uuid=sessuid)
    print(f"===================SAMPLE RETRIEVED {s.uuid}==========================")

    assert(s.title=="SES-01")
    assert(isinstance(s,Session)==True)
    
    s.title="SES-01.1"
    upserted_suid = s.upsert()
    print(f"===================SAMPLE UPSERTED {upserted_suid}==========================")


    assert(upserted_suid==sessuid)
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
    assert(t.field_operator=="echo_operator")
    
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

    ti_many = task_instance_collection.get()
    assert(len(ti_many)>0)
    ti = task_instance_collection.get_one(uuid=task_instance_uid)

    assert(ti.title=="automated-test-task-instance-aa")
    assert(isinstance(ti,TaskInstance)==True)
    upserted_uuid = ti.upsert()
    assert(upserted_uuid==task_instance_uid)
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

def test_get_compute_node():
    nuid=create_sample_compute_node()
    node_collection=ComputeNodeCollection(cms_host=crush_host)
    n=node_collection.get_one(uuid=nuid)
    
    assert(n.title=='worker-node-01')
    assert(n.field_username=="scott")    
    assert(n.field_working_directory=="~/scott")
    
    n.delete()
    
def test_allocate_session_to_compute_node():
    proj_collection=ProjectCollection(cms_host=crush_host)
    subj_collection=SubjectCollection(cms_host=crush_host)
    sess_collection=SessionCollection(cms_host=crush_host)

    nuid=create_sample_compute_node()
    node_collection=ComputeNodeCollection(cms_host=crush_host)
    n=node_collection.get_one(uuid=nuid)
    
    puid=create_sample_project()
    project = proj_collection.get_one(uuid=puid)

    suid = create_sample_subject(puid=puid)
    sessuid = create_sample_session(suid=suid)

    pipeline_uid=create_sample_pipeline()
    pipe_collection=PipelineCollection(cms_host=crush_host)
    
    tuid=create_sample_task(pipeline_uid)
    
    project.field_activated_pipelines = [pipeline_uid]
    project.upsert()

    n.allocate_session(sessuid)
    #Let's see if it allocated the task instance to the compute node        
    ti_col = TaskInstanceCollection(cms_host=crush_host,pipeline=pipeline_uid,task=tuid,session=sessuid)
    tis=ti_col.get()

    assert(n.title=='worker-node-01')
    assert(len(tis)==1)

    for ti in tis:
        t=ti_col.get_one(ti)
        t.delete()
    
    
    n.delete()

    sess = sess_collection.get_one(uuid=sessuid)
    sess.delete()

    subj = subj_collection.get_one(uuid=suid)
    subj.delete()

    p = proj_collection.get_one(uuid=puid)
    p.delete()

    