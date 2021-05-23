from aircrushcore.operators.base_operator import BaseOperator
from aircrushcore.operators.slurm_operator import HCPSlurmJob
from aircrushcore.Models import Pipeline,Task
from aircrushcore.crushhost.repository import PipelineRepository,TaskRepository
#from aircrushcore import workflow
import importlib
import traceback
#import aircrushcore

R=None
try:
    R=PipelineRepository(
        endpoint="http://localhost:81/",
        username="crush",
        password="crush"
        )
except:
    traceback.print_exc()

try:
    TaskRepo=TaskRepository(
        endpoint="http://localhost:81/",
        username="crush",
        password="crush"
        )
except:
    traceback.print_exc()

modnames=['pipelines.levman']

for lib in modnames:
    ##globals()[lib]=importlib.import_module(lib)


    pipeline_module=importlib.import_module(lib)    
    pipeline_dict = pipeline_module.__dict__
    try:
        to_import = pipeline_module.__all__
    except AttributeError:
        to_import = [name for name in pipeline_dict if not name.startswith('_')]
        #================ PIPELINES
        pipelines_found=0
        for name in to_import:          
          if isinstance(pipeline_dict[name],Pipeline):   
              pipelines_found=pipelines_found+1 
              P=pipeline_dict[name]
              

        if pipelines_found>1:
            print(f"Pipeline module [{lib}] has too many pipelines defined.  There can be only one")  

        if pipelines_found==1:
            print(f"Parsing [{lib}]")  
            
            R.upsertPipeline(P)
            #=================  TASKS
            
            list_to_upsert={}
            upserted={}
            skipcounter=0
            upsertcounter=0

            for name in to_import:        
                if isinstance(pipeline_dict[name],BaseOperator):  
                    
                    T=Task(pipeline_dict[name].ID,
                        CallingPipeline=P.ID,
                        Parameters=pipeline_dict[name].Parameters,
                        Prerequisites=pipeline_dict[name].Prerequisites)

                    list_to_upsert[T.ID]=T

            while len(list_to_upsert)>0 and (len(list_to_upsert)>skipcounter) and (len(list_to_upsert)>len(upserted)):
                #print(f"HERE:   len(todo):{len(list_to_upsert)}, skipcounter={skipcounter}, done:{len(upserted)}" )
                for T in list_to_upsert:
                    print(f"Upserting {T}")
                    Tobj=list_to_upsert[T]
                    if(Tobj!=None):
                        if len(Tobj.Prerequisites)>0:
                            canpost=True
                            for prereq in Tobj.Prerequisites:
                                if prereq not in upserted:                                    
                                    canpost=False
                                else:
                                    Tobj.Prerequisites[prereq].uuid=upserted[prereq].uuid
                                    print(f"uuid determined for prereq:  {Tobj.Prerequisites[prereq].uuid}")
                            if canpost:
                                #print(f"Can Upsert {T}")#Upsert
                                uuid=TaskRepo.upsertTask(Tobj)
                                print(f"uuid returned:: {uuid}")
                                Tobj.uuid=uuid
                                upserted[T]=Tobj
                                list_to_upsert[T]=None                                
                                upsertcounter=upsertcounter+1
      
                        else:
                            #print(f"Upsert {T}")#Upsert
                            uuid=TaskRepo.upsertTask(Tobj)
                            print(f"uuid returned: {uuid}")
                            Tobj.uuid=uuid
                            upserted[T]=Tobj
                            list_to_upsert[T]=None
                            #list_to_upsert.pop(T)
                            upsertcounter=upsertcounter+1
                #print(f"THERE:   len(todo):{len(list_to_upsert)}, skipcounter={skipcounter}, done:{len(upserted)}" )
                

                    #add to list to post
                    #while lits to post is not empty or list length=#skipped (DAG not acyclic)
                        #iterate list to post while none left
                            #if item has prereqs in list to post
                                #skip
                                #increment number skipped
                            #else 
                                #upsert
                                #remove from list to post
                                #update upsert increment
                        

                   
                    # TaskRepo.upsertTask(T)  

                    
                 