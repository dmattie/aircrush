from ..Models import Task

class BaseOperator:
    Prerequisites={}
    ID=""
    Parameters=""
    Pipeline=""

    def __init__(self,id,**kwargs):
        self.ID=id
        self.Parameters=kwargs

    def setCallingPipeline(self,pipelineID):
        self.Pipeline=pipelineID
        pass
    
    def addPrerequisite(self,Op):
        if(isinstance(Op,BaseOperator)):
            self.Prerequisites[Op.ID]=Op
        else:
            raise Exception("Item passed to BaseOperator.addPrerequisite was not and instance of BaseOperator") 
    def enqueue(self):
        #print(f"Adding operator {self.ID} to queue")
        pass
    def __del__(self):        
        self.enqueue()

    

        #print("Destructor finished")