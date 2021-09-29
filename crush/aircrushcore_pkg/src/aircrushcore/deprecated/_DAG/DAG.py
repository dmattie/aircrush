from aircrushcore.crushhost.dml.dml_task_instance import TaskInstanceRepository
from aircrushcore.crushhost.dml.dml_task import TaskRepository
import random

class DAG():
    
    
    def __init__(self,host,**kwargs):  

        self.host=host

        pass
    def Advance(self,**kwargs):
        print(f"Advancing all DAGs")
        TIs = self.getReadyTaskInstances(host=self.host)
        print(f"Found {len(TIs)} tasks instances that can be advanced")

        for t in TIs:
            self.invokeTask(t)


    def invokeTask(self,tid,**kwargs):
        

        TIR=TaskInstanceRepository(host=self.host)
        TR=TaskRepository(host=self.host)
        
        ti = TIR.get(uuid=tid)[tid]
        t = TR.get(tid=ti.field_task)
        

        print(f"\tInvoking: {tid}, {ti.title}, {ti.field_task}, {t.field_operator},{t.field_parameters}")

    def getAvailableWorker(self):
        Workers={}
        
    def getReadyTaskInstances(self,**kwargs):
        TIs={}
       
        TIR=TaskInstanceRepository(host=self.host)
        TIs=TIR.get(filter="filter[or-group][group][conjunction]=OR" \
                    "&filter[notstarted-filter][condition][path]=field_status" \
                    "&filter[notstarted-filter][condition][value]=notstarted" \
                    "&filter[notstarted-filter][condition][memberOf]=or-group" \
                    "&filter[failed-group][group][conjunction]=AND" \
                    "&filter[failed-filter][condition][path]=field_status" \
                    "&filter[failed-filter][condition][value]=failed" \
                    "&filter[failed-filter][condition][memberOf]=failed-group" \
                    "&filter[retries-filter][condition][path]=field_remaining_retries" \
                    "&filter[retries-filter][condition][operator]=>" \
                    "&filter[retries-filter][condition][value]=0" \
                    "&filter[retries-filter][condition][memberOf]=failed-group" \
                    "&filter[failed-group][condition][memberOf]=or-group")

        return TIs
        