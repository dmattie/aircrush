import inspect,os

class Pipeline():
        
    def __init__(self,**kwargs):  


        self.title=""
        self.author=""
        self.author_email=""
        self.abstract=""   
        self.uuid=""
        self.plugin_warnings=""     
        if 'metadata' in kwargs:
            m=kwargs['metadata']

        if "id" in m:
            self.ID=m['id']
        else:
            filename=os.path.splitext(os.path.basename(inspect.stack()[1].filename ))[0]
            print("----------------")        
            print(filename)
            print("----------------")
            self.ID=filename
                        
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

        if 'metadata' in kwargs:
            m=kwargs['metadata']
                    

        if 'CallingPipeline' in m:
            self.CallingPipeline=m['CallingPipeline']
        if 'Parameters' in m:
            self.Parameters=m['Parameters']

        if 'Prerequisites' in m:
            self.Prerequisites=m['Prerequisites']
        if 'uuid' in m:
            self.uuid=m['uuid']
            

