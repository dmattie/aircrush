from . import authentication
import sys
import requests
import json

class crush:

    def __init__(self,**kwargs):
        self.username=kwargs['username']
        self.password=kwargs['password']
        self.endpoint=kwargs['endpoint']      
        self.connection=authentication.crushConnection(
          endpoint=self.endpoint,
          username=self.username,
          password=self.password)
        self.session=self.connection.getConnectionToken()

    def get(self,url):
      head = {"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json","X-CSRF-Token":self.connection.csrf_token}
      url=f"{self.connection.endpoint}{url}"
      r = self.session.get(url, headers=head)
      return r

    def patch (self,url,payload):
      head = {"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json","X-CSRF-Token":self.connection.csrf_token}
      url=f"{self.connection.endpoint}{url}"
      r = self.session.patch(url, json.dumps(payload), headers=head)
      return r

    def post (self,url,payload):
      head = {"Accept":"application/vnd.api+json","Content-Type":"application/vnd.api+json","X-CSRF-Token":self.connection.csrf_token}
      url=f"{self.connection.endpoint}{url}"
      print(self.session)
      r = self.session.post(url, json.dumps(payload), headers=head)
      
      return r      
