from .. import crush
from aircrushcore.Models.Project import Project
import traceback

class ProjectRepository():
    
    
    def __init__(self,**kwargs):    
        self.Projects={}    
        if "host" in kwargs:
            self.HOST=kwargs['host']
            self.getKnownProjects()

        else:
            print("\nERROR:ProjectRepository::HOST not specified\n")
            
    def getKnownProjects(self):
        r = self.HOST.get('jsonapi/node/project')
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("ProjectRepository:: No Projects found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--project'):

                        uuid=item['id']

                        activepipelines=[]

                        for ap in item['relationships']['field_activated_pipelines']['data']:                            
                            if ap['type']=='node--pipeline':                                
                                activepipelines.append(ap['id'])

                        metadata={    
                            "title":item['attributes']['title']  ,                            
                            "field_host":item['attributes']['field_host'] ,   
                            "field_username":item['attributes']['field_username'],
                            "field_password":item['attributes']['field_password'],
                            "field_path_to_crush_agent":item['attributes']['field_path_to_crush_agent'],
                            "field_path_to_exam_data":item['attributes']['field_path_to_exam_data'],
                            "field_activated_pipelines":activepipelines ,   
                            "body":item['attributes']['body'],
                            "uuid":uuid                                              
                        }                       

                        self.Projects[item['id']]=Project(metadata=metadata)   

            
            return self.Projects                     

   