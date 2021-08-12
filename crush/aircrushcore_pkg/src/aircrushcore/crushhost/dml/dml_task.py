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

    def get(self,tid): 
        
        #http://localhost:81/jsonapi/node/task_instance?filter[id][value]=64d7003c-848f-42e0-9f42-2f32d54664ea
        r = self.HOST.get(f"jsonapi/node/task?filter[id][value]={tid}")
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print(f"TaskRepository:: Task {tid} not found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:                 

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
                        "field_operator":item['attributes']['field_operator'],
                        "uuid":uuid                                              
                    }                  

                            

                    T=Task(metadata=metadata)   

            
                    return T                    
       
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
                            "field_operator":item['attributes']['field_operator'],
                            "uuid":uuid                                              
                        }                  

                              

                        self.Tasks[uuid]=Task(metadata=metadata)   

            
            return self.Tasks                     

   