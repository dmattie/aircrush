from ..Models import Task

class BaseOperator:

    def __init__(self,id,**kwargs):
        self.ID=id        
        self.Parameters=kwargs
        self.Prerequisites={}
        self.Pipeline=""
        #Set default container
        self.Container="library://dmattie/default/test-a:sha256.877c6589259369c18c0da0f56f9d344256b1ac6221203854aa2d392cc5835d92"

    def setCallingPipeline(self,pipelineID):
        self.Pipeline=pipelineID
        pass
    
    def addPrerequisite(self,Op):        
        if(isinstance(Op,BaseOperator)):            
            self.Prerequisites[Op.ID]=Op
        else:
            raise Exception("Item passed to BaseOperator.addPrerequisite was not and instance of BaseOperator") 
