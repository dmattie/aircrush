
class TaskInstance():
    
    def __init__(self,**kwargs):
               
        self.title=""  
        self.field_associated_participant_ses=""
        self.field_pipeline=""
        self.body=""
        self.field_remaining_retries=""
        self.field_status=""
        self.field_task=""
    
        if 'metadata' in kwargs:
            m=kwargs['metadata']   
                
            if 'title' in m:
                self.title=m['title']        
            if 'field_associated_participant_ses' in m:
                self.field_associated_participant_ses=m['field_associated_participant_ses']
            if 'field_pipeline' in m:
                self.field_pipeline=m['field_pipeline']
            if 'body' in m:
                self.body=m['body']
            if 'field_remaining_retries' in m:
                self.field_remaining_retries=m['field_remaining_retries']
            if 'field_status' in m:
                self.field_status=m['field_status']
            if 'field_task' in m:
                self.field_task=m['field_task']