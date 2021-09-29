import pytest
from aircrushcore.compute.compute_node_connection import ComputeNodeConnection
from aircrushcore.compute.compute import Compute
from aircrushcore.controller.configuration import AircrushConfig
import re

#from aircrushcore.compute.compute_node_connection import ComputeNodeConnection



crush_config='crush.ini'
aircrush=AircrushConfig(crush_config)

endpoint=aircrush.config['COMPUTE']['hostname']
username=aircrush.config['COMPUTE']['username']
password=aircrush.config['COMPUTE']['password']
container=aircrush.config['COMPUTE']['container']
sbatch_submitted_regex=aircrush.config['REGEX']['SBatchSubmitted']

def test_invoke_blocking():    
    conn=ComputeNodeConnection(hostname=endpoint,username=username,password=password,working_directory="~/scratch/.aircrush/")
    node=Compute(conn)
    response = node.invoke_blocking(container=f"{container}",mode="exec", command="whoami")
    assert(response['exit_status']==0)
        # response['env']
        # response['command']
        # response['subsystem']
        # response['exit_status']
        # response['exit_signal']
        # response['returncode']
        # response['stdout']
        # response['stderr']

    #assert(response['stdout']==f"{username}\n")
        


def test_invoke_nonblocking():    
    conn=ComputeNodeConnection(hostname=endpoint,username=username,password=password,working_directory="~/scratch/.aircrush/")
    node=Compute(conn)
    response = node.invoke_nonblocking(container="library://dmattie/default/image:sha256.5146a3230920d96f5b1f0ed97ada6b6ff0545acb36b1841a31250893791af380",
        mode="exec", 
        command="sleep 5;echo Completed",
        working_directory=conn.working_directory,
        account=f"def-{username}",#TODO

    )
    assert(response['exit_status']==0)
    assert(response['job_id']!='None')
    assert(response['job_guid']!='None')

    assert(False)

def test_regex():
    stdout="/home/dmattie/scratch/.aircrush/bd7940bf-a1e2-4d4d-aa0b-b2df8a439d23\nSubmitted batch job 13173622\n"
    guid=None
    jobid=None
    rx = re.compile(sbatch_submitted_regex,re.MULTILINE)
    #rx_result=re.search(stout)
    for match in rx.finditer(stdout):        
        if len(match.groups()) == 2:
            #we found guid and job id            
            guid = match.groups()[0]
            jobid= match.groups()[1]
            print(f"jobid:{jobid}, guid:{guid}")
    
    assert(guid=="bd7940bf-a1e2-4d4d-aa0b-b2df8a439d23")
    assert(jobid=="13173622")
