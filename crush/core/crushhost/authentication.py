import sys,os
import pickle
import requests
import json
import configparser
import tempfile




class crushConnection:
    def __init__(**kwargs):#endpoint,username,password,):
        self.endpoint=endpoint
        self.username=username
        self.password=password
        self.tmp=tempfile.gettempdir()

    csrf_token=""
    logout_token=""
    endpoint=""
    Session=requests.Session()

    def getConnectionToken(self):

        #config = configparser.ConfigParser()
        #config.read('../../crush.ini')

        #self.endpoint=config['REST']['endpoint']
        #u=self.username#config['REST']['username']
        #p=self.password#config['REST']['password']

        #picklelocation=config['PICKLE']['session']
        picklelocation=f"{self.tmp}/crush-session.pickle"

        if os.path.isfile(picklelocation):
            with open(picklelocation, 'rb') as f:
                self.Session = pickle.load(f)
                head={"Content-type": "application/vnd.api+json" }
                url=f"{self.endpoint}user/login_status?_format=json"            
                r = self.Session.get(url,headers=head)#, headers=head)#,auth=(u, p))
                login_status=r.content.decode("utf-8")                

                if self.csrf_token=="":

                    #print('no csrf token found, authenticating')
                    head={"Content-type": "application/json","Accept":"*/*" }
                    url=f'{self.endpoint}/session/token'
                    
                    r = self.Session.get(url)
                    self.csrf_token=r.content

                if login_status!='1':
                    head={"Content-type": "application/vnd.api+json" }
                    url=f"{self.endpoint}user/login?_format=json"            
                    payload='{"name":"%s","pass":"%s"}' %(self.username,self.password)            
                    r = self.Session.post(url, payload,headers=head)#, headers=head)#,auth=(u, p))
                    self.csrf_token=r.json()['csrf_token']
                    self.logout_token=r.json()['logout_token']

                    with open(picklelocation, 'wb') as f:
                        pickle.dump(self.Session, f, pickle.HIGHEST_PROTOCOL)                
                        return(self.Session)
                
               # self.csrf_token=r.json()['csrf_token']
               # self.logout_token=r.json()['logout_token']

        else:
            
                
            if self.csrf_token=="":

                #print('no csrf token found, authenticating')
                head={"Content-type": "application/json","Accept":"*/*" }
                url=f'{self.endpoint}/session/token'
                
                r = self.Session.get(url)
                self.csrf_token=r.content
            
            if self.logout_token=="":
                
                head={"Content-type": "application/vnd.api+json" }
                url=f"{self.endpoint}user/login?_format=json"            
                payload='{"name":"%s","pass":"%s"}' %(self.username,self.password)            

                r = self.Session.post(url, payload,headers=head)#, headers=head)#,auth=(u, p))

                self.csrf_token=r.json()['csrf_token']
                self.logout_token=r.json()['logout_token']


            with open(picklelocation, 'wb') as f:
                pickle.dump(self.Session, f, pickle.HIGHEST_PROTOCOL)                                
                return(self.Session)

        
        return self.Session

            

