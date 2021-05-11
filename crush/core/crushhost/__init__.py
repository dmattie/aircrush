from . import authentication
class crush:

    def __init__(self,username,password,endpoint):
      #  self.username=username
      #  self.password=password
      #  self.endpoint=endpoint
        self.connection=authentication.crushConnection(endpoint,username,password)