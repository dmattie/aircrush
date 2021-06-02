from .. import crush
from aircrushcore.Models.Task import Task
import traceback

class TaskRepository():
    
    
    def __init__(self,**kwargs):    
        self.Tasks={}    
        if "host" in kwargs:
            self.HOST=kwargs['host']
            self.getKnownTasks()

        else:
            raise Exception("ERROR:TaskRepository::HOST not specified on constructor")
            
    def getKnownTasks(self):
        
        r = self.HOST.get('jsonapi/node/task')
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("TaskRepository:: No Tasks found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--task'):

                        uuid=item['id']
                        prereqs=[]

                        for prereq in item['relationships']['field_prerequisite_tasks']['data']:                            
                            if prereq['type']=='node--task':                                
                                prereqs.append(prereq['id'])

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_pipeline":item['relationships']['field_pipeline']['data']['id'],   
                            "field_id":uuid,
                            "field_parameters":item['attributes']['field_parameters'],
                            "field_prerequisite_tasks":prereqs,
                            "uuid":uuid                                              
                        }                  

                              

                        self.Tasks[uuid]=Task(metadata=metadata)   

            
            return self.Tasks                     

   