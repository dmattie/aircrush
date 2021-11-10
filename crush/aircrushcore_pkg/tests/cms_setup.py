from aircrushcore.cms import *
import configparser
import uuid


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
            "field_host":"localhost" ,   
            "field_password":"shinyGiraffe",
            "field_path_to_crush_agent":"test path to crush agent",
            "field_path_to_exam_data":"test path to exam data",
            "field_username":"dmattie",
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
        "field_operator":"echo_operator",
        "field_prerequisite_tasks":[],
        "cms_host":crush_host,
        "field_pipeline":puid
    }
    t = Task(metadata=metadata)
    tuid=t.upsert()
    return tuid

def create_sample_compute_node():
    metadata={
        "title":"worker-node-01",
        "field_host":"localhost",
        "field_username":"scott",
        "field_password":"tiger",
        "field_working_directory":"~/scott",        
        "cms_host":crush_host        
    }
    n = ComputeNode(metadata=metadata)
    nuid=n.upsert()
    print(f"Node created {nuid}")
    return nuid

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