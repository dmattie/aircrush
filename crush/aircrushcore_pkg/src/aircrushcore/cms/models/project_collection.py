
from aircrushcore.cms.models.host import Host
from .project import Project


class ProjectCollection():
    def __init__(self,cms_host:Host):
        self.HOST = cms_host
        self.Projects={} 

    def get_one(self,uuid:str):
        col=self.get(uuid=uuid)
        p = col[list(col)[0]]
        return p
        
    def get(self,**kwargs):


        if 'uuid' in kwargs:
            uuid=kwargs['uuid']        
            filter=f"filter[id][value]={uuid}"
        else:
            filter=""

        url=f"jsonapi/node/project?{filter}"

        r = self.HOST.get(url)
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
                            "uuid":uuid,
                            "cms_host":self.HOST                                             
                        }                       

                        self.Projects[item['id']]=Project(metadata=metadata)   

            
            return self.Projects                     


