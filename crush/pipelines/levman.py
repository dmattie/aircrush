from operators import HCPSlurmJob


pipeline={    
    "id":"levman",
    "title":"Diffusion tractography - all regions"    
    "author":"dave",
    "author-email":"dmattie@stfx.ca",
    "abstract":"A cartesian product of all ROIs producing a large dataframe, one row per exam session, thousands of columns"
    "tasks":{
        "reconall":{            
            "prerequisites":[]
        },
        "registration":{            
            "prerequisites":["reconall"]
        },
        "cartesian":{
            "prerequisites":["registration"]
        }

    }
}

def reconall():
    pass

def registration():
    pass

def cartesian():
    pass