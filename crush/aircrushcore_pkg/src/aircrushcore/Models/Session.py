
class Session():
    
    def __init__(self,**kwargs):
               
        self.title=""                
        self.field_participant=""
        self.field_status=""
        self.uuid=""

        if 'metadata' in kwargs:
            m=kwargs['metadata']
        if 'title' in m:
            self.title=m['title']
        if 'field_participant' in m:
            self.field_participant=m['field_participant']
        if 'field_status' in m:
            self.field_status=m['field_status']      
        if 'uuid' in m:
            if m['uuid'] != "":
                self.uuid=m['uuid']
