from aircrushcore.operators.base_operator import BaseOperator
from aircrushcore.operators.slurm_operator import HCPSlurmJob
from aircrushcore.Models import Pipeline,Task
from aircrushcore.crushhost.repository import PipelineRepository,TaskRepository
from aircrushcore.crushhost.crush import crush

#from aircrushcore import workflow
import importlib
import traceback
#import aircrushcore

crushHOST=None

try:
    crushHOST=crush(
        endpoint="http://localhost:81/",
        username="crush",
        password="crush"
        )
except:
    traceback.print_exc()
    print("\n\n==========\nERROR: Unable to connect to crush host\n==========\n\n")
    
R=None
try:
    R=PipelineRepository(host=crushHOST)
except:
    traceback.print_exc()

try:
    TaskRepo=TaskRepository(host=crushHOST)
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
                    

                    metadata={    
                        "CallingPipeline":P.ID ,  
                        "Parameters":pipeline_dict[name].Parameters,
                        "Prerequisite":pipeline_dict[name].Prerequisites
                    }
                            
                    T=Task(pipeline_dict[name].ID,metadata=metadata)
                    list_to_upsert[T.ID]=T

            while len(list_to_upsert)>0 and (len(list_to_upsert)>skipcounter) and (len(list_to_upsert)>len(upserted)):                
                for T in list_to_upsert:                    
                    Tobj=list_to_upsert[T]
                    if(Tobj!=None):
                        if len(Tobj.Prerequisites)>0:
                            canpost=True
                            for prereq in Tobj.Prerequisites:
                                if prereq not in upserted:                                    
                                    canpost=False
                                else:
                                    Tobj.Prerequisites[prereq].uuid=upserted[prereq].uuid                                                                        
                            if canpost:   
                                ## Careful, there are two of these, this, and the one below for cases without prereqs                             
                                uuid=TaskRepo.upsertTask(Tobj)                                  
                                Tobj.uuid=uuid
                                upserted[T]=Tobj
                                list_to_upsert[T]=None                                
                                upsertcounter=upsertcounter+1
      
                        else:         
                            ## Careful, there are two of these, this, and the one above for cases with prereqs                   
                            uuid=TaskRepo.upsertTask(Tobj)                            
                            Tobj.uuid=uuid
                            upserted[T]=Tobj
                            list_to_upsert[T]=None                            
                            upsertcounter=upsertcounter+1
                