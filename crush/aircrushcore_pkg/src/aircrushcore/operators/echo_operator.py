from .base_operator import BaseOperator
import datetime

class Echo(BaseOperator):
    
    def __init__(self,id,**kwargs):  
        super().__init__()
        self.container="library://dmattie/default/test-a:sha256.877c6589259369c18c0da0f56f9d344256b1ac6221203854aa2d392cc5835d92"              
        
        
    def execute(self,**kwargs):
        #Invocation INFO
        now = datetime.datetime.now()
        print("\nInvoking operator: Echo===========")
        print(f"Singularity Container:{self.container}")
        print(f"Current date and time: {str(now)}")
        print("Parameters passed:")
        for k in kwargs:
            print(f"\t{k}={kwargs[k]}")
        print("End of Echo=======================\n")

        #Execute
        super().pullContainer
