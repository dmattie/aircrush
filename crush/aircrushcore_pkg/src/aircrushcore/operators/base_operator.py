class BaseOperator:
    def __init__(self,id,**kwargs):
        self.ID=id
        
        pass
    def setCallingPipeline(self,pipelineID):
        self.Pipeline=pipelineID
        pass
    def enqueue(self):
        #print(f"Adding operator {self.ID} to queue")
        pass
    def __del__(self):
        self.enqueue()

        #print("Destructor finished")