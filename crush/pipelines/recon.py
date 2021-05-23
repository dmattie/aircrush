from aircrushcore.Models import Pipeline
from aircrushcore.operators.slurm_operator import HCPSlurmJob

metadata={    
    "title":"Recon-All"  ,  
    "author":"Dave Mattie",
    "author_email":"dmattie@stfx.ca",
    "abstract":"Performs recon-all on BIDS compliant subject directories",  
}

pipeline=Pipeline(metadata=metadata)

ta=HCPSlurmJob(id='recon',key='val')   
