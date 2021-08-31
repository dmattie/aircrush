import asyncio, asyncssh, sys
import traceback
import configparser
from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.compute.compute_node_connection import ComputeNodeConnection

class Compute():  

    def __init__(self,conn:ComputeNodeConnection):
        
        self.connection = conn

    def invoke(self, container:str,command:str):
        response={}   

        # asyncio.get_event_loop().run_until_complete(
        #         self._run_ssh_client(
        #             host=self.connection.hostname,
        #             username=self.connection.username,
        #             password=self.connection.password,                
        #             cmd=command                    
        #         )
        #     )  

        asyncio.get_event_loop().run_until_complete(
                self._run_ssh_client(
                    host="localhost",
                    username="dmattie",
                    password="shinyGiraffe",                
                    cmd="whoami"                    
                )

         
        )  
               
        response['env']=self.agentresult.env
        response['command']=self.agentresult.command
        response['subsystem']=self.agentresult.subsystem
        response['exit_status']=self.agentresult.exit_status
        response['exit_signal']=self.agentresult.exit_signal
        response['returncode']=self.agentresult.returncode
        response['stdout']=self.agentresult.stdout
        response['stderr']=self.agentresult.stderr

        return response    
                                    

    async def _run_ssh_client(self,host:str,username:str,password:str,cmd:str):
        

        async with asyncssh.connect(host=host,username=username, password=password, known_hosts=None) as conn:            
            self.agentresult = await conn.run(cmd, check=True)
    
    
        
                                
