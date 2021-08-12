
class Task():
    
    def __init__(self,**kwargs):
               
        self.title=""  
        self.field_pipeline=""
        self.field_id=""
        self.field_parameters=""
        self.field_prerequisite_tasks=""
    
        if 'metadata' in kwargs:
            m=kwargs['metadata']   
        if 'title' in m:
            self.title=m['title']        
        if 'field_pipeline' in m:
            self.field_pipeline=m['field_pipeline']
        if 'field_id' in m:
            self.field_id=m['field_id']
        if 'field_parameters' in m:
            self.field_parameters=m['field_parameters']
        if 'field_prerequisite_tasks' in m:
            self.field_prerequisite_tasks=m['field_prerequisite_tasks']
        if 'field_operator' in m:
            self.field_operator=m['field_operator']