from aircrushcore.crushhost.crush import crush
from aircrushcore.crushhost.sync import plugins
from aircrushcore.crushhost.sync import sync_participant
from aircrushcore.crushhost.sync import sync_task
import traceback


try:
    crushHOST=crush(
        endpoint="http://localhost:81/",
        username="crush",
        password="crush"
        )

    #Look at the pipelines plugin directory and add to Crush Host
   # plugins.sync(crushHOST)

    #Look for any data in the defined projects and sync participants and sessions
   # sync_participant.sync(crushHOST)
    sync_task.sync(crushHOST)


except:
    traceback.print_exc()
    print("\n\n==========\nERROR: Unable to connect to crush host\n==========\n\n")
    exit
    
