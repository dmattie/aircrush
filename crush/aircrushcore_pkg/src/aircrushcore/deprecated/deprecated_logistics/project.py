import asyncio, asyncssh, sys
import uuid

class project():
    self.field_host=""
    self.field_username=""
    self.field_password=""
    self.field_path_to_exam_data=""

    def __init__(field_host,field_username,field_password,field_path_to_exam_data,**kwargs):
        self.field_host=field_host
        self.field_username=field_username
        self.field_password=field_password
        self.field_path_to_exam_data=field_path_to_exam_data

 