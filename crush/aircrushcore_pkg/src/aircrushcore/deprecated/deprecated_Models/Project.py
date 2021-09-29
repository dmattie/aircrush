
class Project():
    
    def __init__(self,**kwargs):
               
        self.title=""                
        self.field_connection_type=""
        self.field_host=""
        self.field_password=""
        self.field_path_to_crush_agent=""
        self.field_path_to_exam_data=""
        self.field_username=""
        self.body=""
        self.id=""

        if 'metadata' in kwargs:
            m=kwargs['metadata']

        if 'title' in m:
            self.title=m['title']
        if 'field_connection_type' in m:
            self.field_connection_type=m['field_connection_type']
        if 'field_host' in m:
            self.field_host=m['field_host']      
        if 'field_password' in m:
            self.field_password=m['field_password']
        if 'field_path_to_crush_agent' in m:            
            self.field_path_to_crush_agent=m['field_path_to_crush_agent']
        if 'field_path_to_crush_agent' in m:
            self.field_path_to_exam_data=m['field_path_to_exam_data']
        if 'field_path_to_exam_data' in m:
            self.field_path_to_crush_agent=m['field_path_to_crush_agent']
        if 'field_username' in m:            
            self.field_username=m['field_username']                     
        if 'body' in m:
            self.body=m['body']     
        if "uuid" in m:
            self.uuid=m['uuid']        
        if "field_activated_pipelines" in m:
            self.field_activated_pipelines=m['field_activated_pipelines']    