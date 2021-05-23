
class Pipeline():
        
    def __init__(self,id,**kwargs):  
        self.ID=id          
        self.title=""
        self.author=""
        self.author_email=""
        self.abstract=""   
        self.uuid=""     
        if 'metadata' in kwargs:
            m=kwargs['metadata']
            
        if 'title' in m:
            self.title=m['title']
        else:
            self.title=id

        if 'author' in m:
            self.author=m['author']

        if 'author_email' in m:
            self.author_email=m['author_email']
        
        if 'abstract' in m:
            self.abstract=m['abstract']

        if 'uuid' in m:
            self.uuid=m['uuid']

    def __enter__(self):
             
        #self.dump()
        

        pass
    def __exit__(self, exc_type, exc_val, exc_tb):
        #print(locals())
        
        pass
    def dump(self):
        print(f"ID:  {self.ID}")
        print(f"Title: {self.title}")
        print(f"Author: {self.author}")
        print(f"Author Email: {self.author_email}")
        print(f"Abstract: {self.abstract}")
        
        functions=[f for f in dir(self) if not f.startswith('_')] 
        print(functions)
        print("xxxxxxxxxx")
        print(locals())

class Task():

    def __init__(self,ID,**kwargs):
        self.ID=ID            
        self.CallingPipeline=""
        self.CallingPipelineUUID=""
        self.Prerequisites={}
        self.log=""
        self.Parameters=""
        self.uuid=""

        if 'CallingPipeline' in kwargs:
            self.CallingPipeline=kwargs['CallingPipeline']
        if 'Parameters' in kwargs:
            self.Parameters=kwargs['Parameters']

        if 'Prerequisites' in kwargs:
            self.Prerequisites=kwargs['Prerequisites']

