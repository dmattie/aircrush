from . import crush
from ..Models import Pipeline,Task
import traceback

class PipelineRepository():
    
    
    def __init__(self,**kwargs):    
        self.Pipelines={}    
        if "host" in kwargs:
            self.HOST=kwargs['host']
            self.getKnownPipelines()
        else:
            print("\nERROR:PipelineRepository::HOST not specified\n")
            

        

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
                            "uuid":uuid,
                            "id": item['attributes']['field_id']                       
                        }

                        self.Pipelines[item['attributes']['field_id']]=Pipeline(metadata=metadata)                        

    def upsertPipeline(self,pipeline):
        
        try:            
            if pipeline.ID in self.Pipelines:
                print(f"PipelineRepository::found profile for [{pipeline.ID}] on CRUSH host, updating metadata")
                
                
                payload = {
                    "data" : {
                        "type":"node--pipeline",    
                        "id":self.Pipelines[pipeline.ID].uuid,                
                        "attributes":{
                            "title": pipeline.title,                        
                            "field_id":pipeline.ID,
                            "field_author":pipeline.author,
                            "field_author_email":pipeline.author_email,
                            "body":pipeline.abstract,
                            "field_plugin_warnings":pipeline.plugin_warnings                            
                        }            
                    }
                }
                                
                r= self.HOST.patch(f"jsonapi/node/pipeline/{self.Pipelines[pipeline.ID].uuid}",payload)
                if(r.status_code!=200):                   
                    print(f"[ERROR] failed to patch pipeline {pipeline.ID} on CRUSH HOST: {r.status_code},  {r.reason}")
                else:                                     
                    if len(r.json()['data'])==0:
                        print("PipelineRepository::UpsertPipeline:  Pipeline not updated.")                
                    else:       
                        return r.json()['data']['id']
                    
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
        if "host" in kwargs:
            self.HOST=kwargs['host']

            self.getKnownTasks()

            PR=PipelineRepository(host=self.HOST)
            PR.getKnownPipelines()
            self.KnownPipelines=PR.Pipelines
            
        else:
            print("\nERROR:TaskRepository::HOST not specified\n")
            

            
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
                            "Prerequisite":item['relationships']['field_prerequisite_tasks']['data'] ,  
                            "uuid":uuid
                        }
                                                                   
                        self.Tasks[item['attributes']['field_id']]=Task(item['attributes']['field_id'] ,metadata=metadata)                        



    def upsertTask(self,task):
        
        try:            
            if task.ID in self.Tasks:                
                print(f"TaskRepository::found task profile for [{task.ID}] uuid:[{self.Tasks[task.ID].uuid}] on CRUSH host, syncing metadata")

                for p in self.KnownPipelines:
                    if self.KnownPipelines[p].ID==task.CallingPipeline:
                        task.CallingPipelineUUID=self.KnownPipelines[p].uuid

                prereq=list()
                for p in task.Prerequisites:                    
                    x={"type":"node--task", "id":task.Prerequisites[p].uuid}                   
                    prereq.append(x)

                payload = {
                    "data" : {
                        "type":"node--task",    
                        "id":self.Tasks[task.ID].uuid,                
                        "attributes":{
                            "title": task.ID,                        
                            "field_id":task.ID,
                            "field_parameters": str(task.Parameters),
                        },
                        "relationships":{
                            "field_pipeline":{
                                "data":{
                                    "type":"node--pipeline",
                                    "id":task.CallingPipelineUUID
                                }
                            },
                            "field_prerequisite_tasks":{
                                "data": prereq#task.Prerequisites                            
                            }
                        }              
                    }
                }

                               
                
                r= self.HOST.patch(f"jsonapi/node/task/{self.Tasks[task.ID].uuid}",payload)
                if(r.status_code!=200):                   
                    print(f"[ERROR] failed to patch task {task.ID} on CRUSH HOST: {r.status_code},  {r.reason}")
                else:                    
                    if len(r.json()['data'])==0:
                        print("TaskRepository::UpsertTask:  Task not created.")                
                    else:       
                        return r.json()['data']['id']
                    
                #Update
            else:
                print(f"TaskRepository::New {task.ID}, Inserting")
                #Insert

                for p in self.KnownPipelines:
                    if self.KnownPipelines[p].ID==task.CallingPipeline:
                        task.CallingPipelineUUID=self.KnownPipelines[p].uuid

                prereq=list()
                for p in task.Prerequisites:
                    x={"type":"node--task", "id":task.Prerequisites[p].uuid}                   
                    prereq.append(x)
                
                
                payload = {"data" : {
                    "type":"node--task",                    
                    "attributes":{
                        "title": task.ID,                        
                        "field_id":task.ID,
                        "field_parameters": str(task.Parameters),
                    },
                    "relationships":{
                        "field_pipeline":{
                            "data":{
                                "type":"node--pipeline",
                                "id":task.CallingPipelineUUID
                            }
                        },
                        "field_prerequisite_tasks":{
                            "data": prereq#task.Prerequisites                            
                        }
                    }              
                }}

               # print(payload)                

                r= self.HOST.post("jsonapi/node/task",payload)
                if(r.status_code!=201):                   
                    print(f"[ERROR] failed to create task {task.ID} on CRUSH HOST: {r.status_code},  {r.reason}")
                else:
                    print(r.json())
                    if len(r.json()['data'])==0:
                        print("TaskRepository::UpsertTask:  Task not created.")                
                    else:       
                        return r.json()['data']['id']
                    

        except:
            if( not isinstance(task,Task)):
                print("Task object not passed to upsert")
            else:
                 traceback.print_exc()

