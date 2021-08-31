import pytest
from aircrushcore.compute.compute_node_connection import ComputeNodeConnection
from aircrushcore.compute.compute import Compute
from aircrushcore.controller.configuration import AircrushConfig

#from aircrushcore.compute.compute_node_connection import ComputeNodeConnection



crush_config='crush.ini'
aircrush=AircrushConfig(crush_config)

endpoint=aircrush.config['COMPUTE']['hostname'],
username=aircrush.config['COMPUTE']['username'],
password=aircrush.config['COMPUTE']['password']

def test_invoke():    
    conn=ComputeNodeConnection(hostname=endpoint,username=username,password=password)
    node=Compute(conn)
    response = node.invoke(container="abc",command="whoami")
    assert(response['exit_status']==0)
        
    #assert(False)
