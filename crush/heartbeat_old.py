from aircrushcore.crushhost.crush import crush
from aircrushcore.crushhost.sync import plugins
from aircrushcore.crushhost.sync import sync_participant
from aircrushcore.crushhost.sync import sync_task
from aircrushcore.crushhost.dml.dml_project import ProjectRepository
from aircrushcore.crushhost.dml.dml_participant import ParticipantRepository
from aircrushcore.crushhost.dml.dml_compute_node import ComputeNodeRepository
from aircrushcore.DAG.DAG import DAG
import traceback
import configparser


try:

    config = configparser.ConfigParser()
    config.read('crush.ini')
        
    crushHOST=crush(
        endpoint=config['REST']['endpoint'],
        username=config['REST']['username'],
        password=config['REST']['password']
        )
    ############################################################################
    # SYNC EVERYTHING TO PREP FOR NEXT HEARTBEAT
    ############################################################################
    
    #Look at the pipelines plugin directory and add to Crush Host
    ##plugins.sync(crushHOST)

    #Look for any data in the defined projects and sync participants and sessions
    sync_participant.sync(crushHOST)
    sync_task.sync(crushHOST)
    
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
    
