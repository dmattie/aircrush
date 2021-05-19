import sys

from aircrushcore.operators.base_operator import BaseOperator
from aircrushcore.operators.slurm_operator import HCPSlurmJob
from aircrushcore.workflow.pipeline import Pipeline

metadata={    
    "title":"Diffusion tractography - all regions"  ,  
    "author":"dave",
    "author_email":"dmattie@stfx.ca",
    "abstract":"A cartesian product of all ROIs producing a large dataframe, one row per exam session, thousands of columns",  
}

pipeline=Pipeline('levman',metadata=metadata)

t1=HCPSlurmJob(id='hcp1')   

  