import asyncio, asyncssh, sys

with open('/home/dmattie/.ssh/aircrush') as f:
    pkey = f.readlines()


def gzSubject(host,username,key,cmd):
    
    cmd=f"whoami"
    
    asyncio.get_event_loop().run_until_complete(gzSubjectWorker(
        host=host,
        username=username,
        key=key,
        cmd=cmd            
    ))
    
    return uid

async def gzSubjectWorker(host,username,key,cmd):
    print(f"\n\n=================\n\nhost={host}, username={username}, key={key}")
    # async with asyncssh.connect(host=host,username=username, client_keys=key, passphrase='2sneakers',known_hosts=None) as conn:
    #     agentresult = await conn.run(cmd, check=True)            
    #     print(agentresult)            
    # async with asyncssh.connect(host=host,username=username, client_keys=None, known_hosts=None) as conn:
    #     agentresult = await conn.run(cmd, check=True)            
    #     print(agentresult)            
    async with asyncssh.connect(host=host,username=username,password="Alaire399!", client_keys=key, known_hosts=None) as conn:
        agentresult = await conn.run(cmd, check=True)            
        print(agentresult)                           
    pass


x=gzSubject("cedar.computecanada.ca","dmattie",'/home/dmattie/.ssh/id_rsa',"whoami")
# conn = make_connection(host,username,key)

# def make_connection(self, host,username,key):
    
#     return await asyncssh.connect(
#         host,
#         known_hosts=None,
#         username=username,
#         client_keys=key        
#     ) 