from .. import crush
from aircrushcore.Models.ComputeNode import ComputeNode
import traceback

class ComputeNodeRepository():

    def __init__(self,**kwargs):
        
        if "host" in kwargs:
            self.HOST=kwargs['host']
        else:
            print("\nERROR:ComputeNodeRepository::HOST not specified\n")
        self.ComputeNodes=self.get()

    def isAvailable(self,uuid):
        return uuid
        #TODO

    def nextAvailable(self):
        for n in self.ComputeNodes:
            if(self.isAvailable(n)):
                return n

        return None  #nothing available


    def get(self,**kwargs):        
        
        Nodes={}

        if "uuid" in kwargs:            
            filter_uuid=f"&filter[id][value]={kwargs['uuid']}"
            print(filter_uuid)
        else:
            filter_uuid=""
       
                  
        r = self.HOST.get(f'jsonapi/node/compute_node?{filter_uuid}')
        
        if r.status_code==200:  #We can connect to CRUSH host           
              
            if len(r.json()['data'])==0:
                print("ComputeNodeRepository:: No matching compute nodes found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--compute_node'):
                        
                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,                                                        
                            "body":item['attributes']['body'],
                            "field_host":item['attributes']['field_host'],
                            "field_password":item['attributes']['field_password'],
                            "field_username":item['attributes']['field_username'],
                            "field_working_directory":item['attributes']['field_working_directory'],                            
                            "uuid":uuid                                              
                        }

                        Nodes[item['id']]=ComputeNode(metadata=metadata)     
            return Nodes


