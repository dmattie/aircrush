import pytest
from aircrushcore.compute.compute_node_connection import ComputeNodeConnection
from aircrushcore.compute.compute import Compute
from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.dag import Workload
from aircrushcore.cms.task_instance import TaskInstance
from .cms_setup import *
#from aircrushcore.compute import ComputeNodeConnection
import aircrushcore.compute

#from aircrushcore.compute.compute_node_connection import ComputeNodeConnection



crush_config='crush.ini'
aircrush=AircrushConfig(crush_config)

endpoint=aircrush.config['COMPUTE']['hostname'],
username=aircrush.config['COMPUTE']['username'],
password=aircrush.config['COMPUTE']['password']

def test_get_next_task():    
    w=Workload(aircrush)
    task = w.get_next_task()
    assert(w.count_of_incomplete_tasks()>0)
    assert(isinstance(task,TaskInstance))
    
def test_invoke_task():

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
    #INVOKE
    w= Workload(aircrush)
    response = w.invoke_task(ti)
    
    #conn=ComputeNodeConnection(hostname=endpoint,username=username,password=password)
    #node=Compute(conn)
    #response = node.invoke(container="abc",command="whoami")
    assert(response['exit_status']==0)

    print(response)




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

    assert(False)