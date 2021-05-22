from ..Models import Task

class BaseOperator:

    def __init__(self,id,**kwargs):
        self.ID=id
        self.Parameters=kwargs
        self.Prerequisites={}
        self.Pipeline=""

    def setCallingPipeline(self,pipelineID):
        self.Pipeline=pipelineID
        pass
    
    def addPrerequisite(self,Op):        
        if(isinstance(Op,BaseOperator)):            
            self.Prerequisites[Op.ID]=Op
        else:
            raise Exception("Item passed to BaseOperator.addPrerequisite was not and instance of BaseOperator") 
