from aircrushcore.operators.base_operator import BaseOperator
from aircrushcore.workflow.pipeline import Pipeline
from aircrushcore.crushhost.repository import PipelineRepository
#from aircrushcore import workflow
import importlib
import traceback
#import aircrushcore

print("A")
R=None
try:
    R=PipelineRepository(
        endpoint="http://localhost:81/",
        username="crush",
        password="crush"
        )
except:
    traceback.print_exc()


print("B")

modnames=['pipelines.levman']

for lib in modnames:
    ##globals()[lib]=importlib.import_module(lib)


    pipeline_module=importlib.import_module(lib)
    print("X")
    pipeline_dict = pipeline_module.__dict__
    try:
        to_import = pipeline_module.__all__
    except AttributeError:
        to_import = [name for name in pipeline_dict if not name.startswith('_')]

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
               
            
            
            
            #print(pipeline_dict[name].ID)
        

     #     print(f"...............{name}={pipeline_dict[name]}")
     
  #  print(dir())
   #print(type(t1))
   #print(isinstance(t1, BaseOperator))
   #pass

# for lib in modnames:
#     print(lib)
#     for potentialOp in globals()[lib]:#(dir(globals()[lib])):

#         if(isinstance(potentialOp,BaseOperator)):
#             print(potentialOp)
#         else:
#             print("Not:"+potentialOp)
# print('==================')
            
# print(globals())





#from crush import pluginloader

#for i in pluginloader.getPlugins():
#    print(i)           
    #    if(self.ID==None or i["name"]==self.ID):
    #        print("Invoking plugin " + i["name"])
    #        plugin = pluginloader.loadPlugin(i)                
    #        plugin.run(self)