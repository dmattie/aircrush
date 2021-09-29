
class Exam():
    
    def __init__(self,**kwargs):
               
        self.title=""
        self.field_directory_format=""
        self.field_exam_id=""
        self.notes=""
        self.field_project=""
        self.field_session=""
        self.uuid=""

        if 'metadata' in kwargs:
            m=kwargs['metadata']
        if 'title' in m:
            self.title=m['title']
        if 'field_directory_format' in m:
            self.field_directory_format=m['field_directory_format']
        if 'field_exam_id' in m:
            self.field_exam_id=m['field_exam_id']
        if 'notes' in m:
            self.notes=m['notes']
        if 'field_project' in m:
            self.field_project=m['field_project']
        if 'field_sesson' in m:
            self.field_sesson=m['field_session']
        if 'uuid' in m:
            self.uuid=m['uuid']
