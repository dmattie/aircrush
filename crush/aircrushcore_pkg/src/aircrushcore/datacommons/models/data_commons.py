import configparser
import os,sys
from aircrushcore.controller.configuration import AircrushConfig
from aircrushcore.cms.models import *
#from aircrushcore.cms.models.project_collection import ProjectCollection


class DataCommons():  

    def __init__(self,aircrush:AircrushConfig):

        # config = configparser.ConfigParser()
        # config.read(configfile)
        self.commons_path = aircrush.config['COMMONS']['commons_path']
        self.staging_path = aircrush.config['COMMONS']['staging_path']
        self.cms_host=Host(
            endpoint=aircrush.config['REST']['endpoint'],
            username=aircrush.config['REST']['username'],
            password=aircrush.config['REST']['password']
            )
        

    def initialize(self):
        if not os.path.exists(f"{self.commons_path}/projects"):
            os.makedirs(f"{self.commons_path}/projects")  
        if not os.path.exists(f"{self.commons_path}/contrib/pipelines"):
            os.makedirs(f"{self.commons_path}/contrib/pipelines")  
        return True

    # def initialize_project(self,project:Project):
    #     if not os.path.exists(f"{self.commons_path}/projects/{project.field_path_to_exam_data}"):
    #         os.makedir(f"{self.commons_path}/projects/{project.field_path_to_exam_data}")
        

    def Projects(self,active_only = False):
       

        projects=os.listdir(f"{self.commons_path}/projects/")
        if not active_only:
            return projects
        else:
            active_projects=[]
            cms_project_collection = ProjectCollection(cms_host=self.cms_host)
            cms_projects=cms_project_collection.get()
            #print(cms_project_collection)
            for dcProject in projects:
                #print(dcProject)
                for cmsProject in cms_projects:
                    if cmsProject==dcProject:
                        #print('active')
                        active_projects.append(dcProject)
            return active_projects

    def Subjects(self,project: str):

        subjects=os.listdir(f"{self.commons_path}/projects/{project}")
        return subjects

  
            
