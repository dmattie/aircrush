import sys


from aircrushcore.operators.slurm_operator import HCPSlurmJob
from aircrushcore.Models import Pipeline

metadata={    
    "title":"Diffusion tractography - all regions"  ,  
    "author":"dave",
    "author_email":"dmattie@stfx.ca",
    "abstract":"A cartesian product of all ROIs producing a large dataframe, one row per exam session, thousands of columns",  
}

pipeline=Pipeline('levman',metadata=metadata)

t1=HCPSlurmJob(id='hcp1',key='val')   
t2=HCPSlurmJob(id='hcp2')  

  