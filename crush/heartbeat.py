from aircrushcore.operators.base_operator import BaseOperator
from aircrushcore.operators.slurm_operator import HCPSlurmJob
from aircrushcore.Models import Pipeline,Task
from aircrushcore.crushhost.repository import PipelineRepository
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
            for name in to_import:        
                if isinstance(pipeline_dict[name],BaseOperator):      
                    T=Task(pipeline_dict[name].ID)
                    T.CallingPipeline=P.ID
                    T.Parameters=pipeline_dict[name].constructor
                    print(dir(T))
        
                    
                    
                    # ,pipeline_dict[name].constructor)     
                    # print(name) 
                    # parms=pipeline_dict[name].__init__.__code__.co_varnames
                    # print(parms)
                    # print(pipeline_dict[name].constructor)
        