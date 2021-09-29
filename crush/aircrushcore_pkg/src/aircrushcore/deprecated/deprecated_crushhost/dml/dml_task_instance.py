from .. import crush
from aircrushcore.Models.TaskInstance import TaskInstance
import traceback

class TaskInstanceRepository():

    def __init__(self,**kwargs):
        
        if "host" in kwargs:
            self.HOST=kwargs['host']
        else:
            print("\nERROR:TaskInstanceRepository::HOST not specified\n")

    def get(self,**kwargs):        
        # http://localhost:81/jsonapi/node/task_instance?filter[field_associated_participant_ses.id][value]=82b63402-ce08-449b-99c1-6eb3f6688e1c&filter[field_task.id][value]=4d7e2b54-ff0b-4bbe-8d0a-40dd98cd03d8
        Instances={}

        if "uuid" in kwargs:            
            filter_uuid=f"&filter[id][value]={kwargs['uuid']}"
            print(filter_uuid)
        else:
            filter_uuid=""

        if "session" in kwargs:
            filter_session=f"&filter[field_associated_participant_ses.id][value]={kwargs['session']}"
        else:
            filter_session=""

        if "task" in kwargs:
            filter_task=f"&filter[field_task.id][value]={kwargs['task']}"
        else:
            filter_task=""

        if "filter" in kwargs:
            filter_direct=kwargs['filter']
        else:
            filter_direct=""
                  
        r = self.HOST.get(f'jsonapi/node/task_instance?{filter_uuid}{filter_session}{filter_task}{filter_direct}')
        print(f"jsonapi/node/task_instance?{filter_uuid}{filter_session}{filter_task}{filter_direct}")
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("TaskInstanceRepository:: No matching task instances found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--task_instance'):
                        
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_associated_participant_ses":item['relationships']['field_associated_participant_ses']['data']['id'] ,   
                            "field_pipeline":item['relationships']['field_pipeline']['data']['id'],
                            "body":item['attributes']['body'],
                            "field_remaining_retries":item['attributes']['field_remaining_retries'],
                            "field_status":item['attributes']['field_status'],
                            "field_task":item['relationships']['field_task']['data']['id'],
                            "uuid":uuid                                              
                        }

                        Instances[item['id']]=TaskInstance(metadata=metadata)     
            return Instances

    def upsert(self,task_instance):
        print("Upserting task instance")
        try:
            TI = self.get(session=task_instance.field_associated_participant_ses,task=task_instance.field_task)
            if(len(TI)>0):
                print("Task Instance exists; updating {####### TODO #######}")
            else:
                print(f"TaskInstanceRepository::New {task_instance.title}, Inserting")

                payload = {
                    "data" : {
                        "type":"node--task_instance",                                           
                        "attributes":{
                            "title": task_instance.title,                                                    
                            "field_status": task_instance.field_status,
                            "body":task_instance.body,
                            "field_remaining_retries":task_instance.field_remaining_retries,
                            "field_status":task_instance.field_status
                        },
                        "relationships":{
                            "field_associated_participant_ses":{
                                "data":{
                                    "type":"node--session",
                                    "id":task_instance.field_associated_participant_ses
                                }
                            },
                            "field_pipeline":{
                                "data":{
                                    "type":"node--pipeline",
                                    "id":task_instance.field_pipeline
                                }
                            },
                            "field_task":{
                                "data":{
                                    "type":"node--task",
                                    "id":task_instance.field_task
                                }
                            }

                        }              
                    }
                }
                print(payload)
                r= self.HOST.post("jsonapi/node/task_instance",payload)
                if(r.status_code!=201):                   
                    print(f"[ERROR] failed to create task instance {task_instance.title} on CRUSH HOST: {r.status_code},  {r.reason}")
                else:
                    
                    if len(r.json()['data'])==0:
                        print("TaskInstanceRepository::UpsertTaskInstance:  TaskInstance not created.")                
                    else:       
                        return r.json()['data']['id']                    
        except:
            if( not isinstance(task_instance,TaskInstance)):
                print("TaskInstance object not passed to upsert")
            else:
                 traceback.print_exc()

