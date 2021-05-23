from aircrushcore.crushhost.crush import crush
from aircrushcore.crushhost.sync import plugins 
import traceback


try:
    crushHOST=crush(
        endpoint="http://localhost:81/",
        username="crush",
        password="crush"
        )
except:
    traceback.print_exc()
    print("\n\n==========\nERROR: Unable to connect to crush host\n==========\n\n")
    exit
    
plugins.sync(crushHOST)
