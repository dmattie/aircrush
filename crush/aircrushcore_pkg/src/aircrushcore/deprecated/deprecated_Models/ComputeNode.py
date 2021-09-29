
class ComputeNode():
    
    def __init__(self,**kwargs):
               
        self.title=""  
        self.field_host=""
        self.field_password=""
        self.field_username=""
        self.field_working_directory=""
    
        if 'metadata' in kwargs:
            m=kwargs['metadata']   
            if 'title' in m:
                self.title=m['title']
            if 'field_host' in m:
                self.field_host=m['field_host']
            if 'field_password' in m:
                self.field_password=m['field_password']
            if 'field_username' in m:
                self.field_username=m['field_username']
            if 'field_working_directory' in m:
                self.field_working_directory=m['field_working_directory']