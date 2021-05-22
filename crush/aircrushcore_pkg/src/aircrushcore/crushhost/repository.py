from . import crush
from ..Models import Pipeline,Task
import traceback

class PipelineRepository():
    
    
    def __init__(self,**kwargs):    
        self.Pipelines={}    
        username=kwargs['username']
        password=kwargs['password']
        endpoint=kwargs['endpoint']  

        self.HOST=crush.crush(
            endpoint="http://localhost:81/",
            username="crush",
            password="crush"
        )
        self.getKnownPipelines()

    def getKnownPipelines(self):
        r = self.HOST.get('jsonapi/node/pipeline')
        if r.status_code==200:  #We can connect to CRUSH host
            # Iterate the pipelines
            pipeline_count=0    
            if len(r.json()['data'])==0:
                print("PipelineRepository:: No pipelines found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--pipeline'):
                        pipeline_count=pipeline_count+1
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,  
                            "author":item['attributes']['field_author'],
                            "author_email":item['attributes']['field_author_email'],
                            "abstract":item['attributes']['body']['value'],                             
                        }

                        self.Pipelines[item['attributes']['field_id']]=Pipeline(item['attributes']['field_id'] ,metadata=metadata)                        

    def upsertPipeline(self,pipeline):
        
        try:            
            if pipeline.ID in self.Pipelines:
                print(f"PipelineRepository::found profile for [{pipeline.ID}] on CRUSH host, updating metadata")
                pass
                #Update
            else:
                print(f"PipelineRepository::New {pipeline.ID}, Inserting")
                #Insert
 
                payload = {"data" : {
                    "type":"node--pipeline",                    
                    "attributes":{
                        "field_author": pipeline.author, 
                        "title": pipeline.title,
                        "field_author_email":pipeline.author_email,
                        "body":pipeline.abstract,
                        "field_id":pipeline.ID
                    }               
                }}

                r= self.HOST.post("jsonapi/node/pipeline",payload)
                if(r.status_code!=201):
                    print(f"[ERROR] failed to create {ID} on CRUSH HOST: {r.status_code},  {r.reason}")
        except:
            if( not isinstance(pipeline,Pipeline)):
                print("Pipeline object not passed to upsert")
            else:
                 traceback.print_exc()



class TaskRepository():
    
    
    def __init__(self,**kwargs):  
        self.Tasks={}      
        username=kwargs['username']
        password=kwargs['password']
        endpoint=kwargs['endpoint']  

        self.HOST=crush.crush(
            endpoint="http://localhost:81/",
            username="crush",
            password="crush"
        )

        self.getKnownTasks()

    def getKnownTasks(self):
        r = self.HOST.get('jsonapi/node/task')
        if r.status_code==200:  #We can connect to CRUSH host
            # Iterate the tasks            
            task_count=0    
            if len(r.json()['data'])==0:
                print("TaskRepository:: No tasks found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--task'):
                        task_count=task_count+1
                        uuid=item['id']


                        metadata={    
                            "CallingPipeline":item['relationships']['field_pipeline']['data']['id']  ,  
                            "Parameters":item['attributes']['field_parameters'],
                            "Prerequisite":item['relationships']['field_prerequisite_tasks']['data']                          
                        }

                        self.Tasks[item['attributes']['field_id']]=Task(item['attributes']['field_id'] ,metadata=metadata)                        



    def upsertTask(self,task):
        
        try:            
            if task.ID in self.Tasks:
                print(f"TaskRepository::found task profile for [{task.ID}] on CRUSH host, updating metadata")
                pass
                #Update
            else:
                print(f"TaskRepository::New {task.ID}, Inserting")
                #Insert
 
                payload = {"data" : {
                    "type":"node--task",                    
                    "attributes":{
                        "title": task.ID,                        
                        "field_id":task.ID,
                        "field_parameters": task.Parameters,
                    },
                    "relationships":{
                        "field_pipeline":{
                            "data":{
                                "type":"node--pipeline",
                                "id":task.CallingPipeline
                            }
                        },
                        "field_prerequisite_tasks":{
                            "data":[
                                task.Prerequisites
                            ]
                        }
                    }              
                }}

                print(payload)

                r= self.HOST.post("jsonapi/node/task",payload)
                if(r.status_code!=201):
                    print(r)
                    print(f"[ERROR] failed to create task {task.ID} on CRUSH HOST: {r.status_code},  {r.reason}")
        except:
            if( not isinstance(task,Task)):
                print("Task object not passed to upsert")
            else:
                 traceback.print_exc()


