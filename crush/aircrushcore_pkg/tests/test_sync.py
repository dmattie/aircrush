import pytest
from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.controller.sync import Sync
#from .cms_setup import *



crush_config='/Users/dmattie/aircrush/crush/aircrushcore_pkg/tests/crush.ini'
aircrush=AircrushConfig(crush_config)
keys=aircrush.config.sections()
for k in keys:
    print(k)
endpoint=aircrush.config['COMPUTE']['hostname'],
username=aircrush.config['COMPUTE']['username'],
password=aircrush.config['COMPUTE']['password']

#def test_sync(): 

syncro = Sync(aircrush)   

assert(False)
