import sys
sys.path.append('..')

from crush.operators.base_operator import BaseOperator
from crush.operators.slurm_operator import HCPSlurmJob
from crush.Workflow import Pipeline


# pipeline={    
#     "id":"levman",
#     "title":"Diffusion tractography - all regions"  ,  
#     "author":"dave",
#     "author-email":"dmattie@stfx.ca",
#     "abstract":"A cartesian product of all ROIs producing a large dataframe, one row per exam session, thousands of columns",
#     "tasks":{
#         "reconall":{            
#             "prerequisites":[]
#         },
#         "registration":{            
#             "prerequisites":["reconall"]
#         },
#         "cartesian":{
#             "prerequisites":["registration"]
#         }

#     }
# }

class Pipeline('levman'):    
    def __init__(self):
    
        t1=HCPSlurmJob(id='hcp1')
            #https://www.danielmorell.com/blog/dynamically-calling-functions-in-python-safely
        # pipeline.dump()
            #print(locals())
        #  print(dir())
        print(type(t1))
        print(isinstance(t1, BaseOperator))
        pass
    def t0():
        