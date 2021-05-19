
class Pipeline():
    ID=""
    title=""
    author=""
    author_email=""
    abstract=""
        
    def __init__(self,id,**kwargs):
        self.ID=id
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
