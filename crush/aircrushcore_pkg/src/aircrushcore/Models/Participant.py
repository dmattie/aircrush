
class Participant():
    
    def __init__(self,**kwargs):
               
        self.title=""                
        self.field_project=""
        self.field_status=""
        self.uuid=""
        self.isbids=""

        if 'metadata' in kwargs:
            m=kwargs['metadata']
        if 'title' in m:
            self.title=m['title']
        if 'field_project' in m:
            self.field_project=m['field_project']
        if 'field_status' in m:
            self.field_status=m['field_status']      
        if 'uuid' in m:
            self.uuid=m['uuid']
        if 'isbids' in m:
            self.isbids=m['isbids']
