import traceback
import configparser
from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.controller.sync import Sync
from aircrushcore.datacommons.models.data_commons import DataCommons
from aircrushcore.cms.models.project_collection import ProjectCollection
from aircrushcore.cms.models.subject_collection import SubjectCollection
from aircrushcore.cms.models.project import Project
from aircrushcore.cms.models.host import Host
from aircrushcore.controller.health import Health
# from aircrushcore.crushhost.crush import crush
# from aircrushcore.crushhost.sync import plugins
# from aircrushcore.crushhost.sync import sync_participant
# from aircrushcore.crushhost.sync import sync_task
# from aircrushcore.crushhost.dml.dml_project import ProjectRepository
# from aircrushcore.crushhost.dml.dml_participant import ParticipantRepository
# from aircrushcore.crushhost.dml.dml_compute_node import ComputeNodeRepository
# from aircrushcore.DAG.DAG import DAG

try:

    crush_config='crush.ini'
    aircrush=AircrushConfig(crush_config)

    crush_host=Host(
        endpoint=aircrush.config['REST']['endpoint'],
        username=aircrush.config['REST']['username'],
        password=aircrush.config['REST']['password']
        )


    sync=Sync(aircrush)
    dc=DataCommons(aircrush)


    ############################################################################
    # SYNC EVERYTHING TO PREP FOR NEXT HEARTBEAT
    ############################################################################
    
    #Look at the pipelines plugin directory and add to Crush Host
    ##plugins.sync(crushHOST)

    #Look for any data in the defined projects and sync participants and sessions
    sync.sync_projects()
    sync.sync_subject_sessions()

    health=Health(aircrush)
    health.audit()


    
    ############################################################################
    # ADVANCE PIPELINE GRAPHS
    ############################################################################
    # PR=ProjectRepository(host=crushHOST)
    # NodeRepo=ComputeNodeRepository(host=crushHOST)
    
    # projects=PR.getKnownProjects()

    # for p in projects:        
    #     participantRepo = ParticipantRepository(host=crushHOST,project=p)
    #     subjects=participantRepo.getKnownParticipants()
    #     for s in subjects:            
    #         worker=NodeRepo.nextAvailable()
    #         if worker:
    #             participantRepo.assignWorker(projects[p],subjects[s],worker)                
    #         else:
    #             print("Where are currently no worker nodes available")
            
        
    #dag=DAG(host=crushHOST)
    #dag.Advance()


except:
    traceback.print_exc()
    print("\n\n==========\nERROR: Heartbeat had failures\n==========\n\n")
    exit
    
