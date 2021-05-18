from crush.operators.base_operator import BaseOperator
from crush.workflow.pipeline import Pipeline
import importlib


modnames=['pipelines.levman']

for lib in modnames:
    ##globals()[lib]=importlib.import_module(lib)


    my_module=importlib.import_module(lib)

    module_dict = my_module.__dict__
    try:
        to_import = my_module.__all__
    except AttributeError:
        to_import = [name for name in module_dict if not name.startswith('_')]
        for name in to_import:
          print(f"{name}={module_dict[name]}")
          x=type(module_dict[name])
          print(x)
       #   if isinstance(module_dict[name],crush.workflow.pipeline.Pipeline):
       #     print("Found!!")
        


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