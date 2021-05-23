from aircrushcore.Models import Pipeline
from aircrushcore.operators.slurm_operator import HCPSlurmJob

metadata={    
    "title":"Diffusion tractography - all regions"  ,  
    "author":"Dave Mattie",
    "author_email":"dmattie@stfx.ca",
    "abstract":"A cartesian product of all ROIs producing a large dataframe, one row per exam session, thousands of columns",  
}

pipeline=Pipeline(metadata=metadata)

ta=HCPSlurmJob(id='hcp1',key='val')   
tb=HCPSlurmJob(id='hcp2')  
tc=HCPSlurmJob(id='hcp3',a='b')  

tb.addPrerequisite(ta)
tc.addPrerequisite(tb)


  