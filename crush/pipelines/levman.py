from aircrushcore.Models import Pipeline
from aircrushcore.operators.slurm_operator import HCPSlurmJob

metadata={    
    "title":"Diffusion tractography - all regions"  ,  
    "author":"Dave Mattie",
    "author_email":"dmattie@stfx.ca",
    "abstract":"A cartesian product of all ROIs producing a large dataframe, one row per exam session, thousands of columns",  
}

pipeline=Pipeline(metadata=metadata)

ta=HCPSlurmJob(id='registration', cmd="contrib/levman/diskusage_report.sh", time="0:0:5", mem_per_cpu="256M", cpus_per_task="1")   
tb=HCPSlurmJob(id='parcellation')  
tc=HCPSlurmJob(id='preprocessing', time="7:0:0")  
td=HCPSlurmJob(id='trackvis-cartesian',time="8:0:0",cpus_per_task="32", )


tb.addPrerequisite(ta)
tc.addPrerequisite(tb)
td.addPrerequisite(tc)


  