
class Pipeline():
    ID=""
    title=""
    author=""
    author_email=""
    abstract=""
        
    def __init__(self,id,**kwargs):
        self.ID=id
        if 'title' in kwargs:
            self.title=kwargs['title']
        else:
            self.title=id

        if 'author' in kwargs:
            self.author=kwargs['author']

        if 'author-email' in kwargs:
            self.author_email=kwargs['author-email']
        
        if 'abstract' in kwargs:
            self.abstract=kwargs['abstract']

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
