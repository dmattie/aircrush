from .. import crush
from aircrushcore.Models.Exam import Exam
import traceback

class ExamRepository():
    
    
    def __init__(self,**kwargs):    
        self.Exams={}    
        if "host" in kwargs:
            self.HOST=kwargs['host']
            self.getKnownExams()
        else:
            print("\nERROR:ExamRepository::HOST not specified\n")
            

        

    def getKnownExams(self):
        r = self.HOST.get('jsonapi/node/exam')
        if r.status_code==200:  #We can connect to CRUSH host
            # Iterate the pipelines
            pipeline_count=0    
            if len(r.json()['data'])==0:
                print("examRepository:: No exams found on CRUSH Host.")                
            else:       
                for item in r.json()['data']:
                    if(item['type']=='node--exam'):

                        uuid=item['id']

                        metadata={    
                            "title":item['attributes']['title']  ,  
                            "field_directry_format":item['attributes']['field_directory_format'],
                            "field_exam_id":item['attributes']['field_exam_id'],
                            "notes":item['attributes']['body'], 
                            "field_project":item['relationships']['field_project']['data'] , 
                            "field_session" :item['attributes']['field_session'],
                            "uuid":uuid                                              
                        }

                        self.Exams[item['id']]=Exam(metadata=metadata)                        


    # def upsertPipeline(self,pipeline):
        
    #     try:            
    #         if pipeline.ID in self.Pipelines:
    #             print(f"PipelineRepository::found profile for [{pipeline.ID}] on CRUSH host, updating metadata")
                
                
    #             payload = {
    #                 "data" : {
    #                     "type":"node--pipeline",    
    #                     "id":self.Pipelines[pipeline.ID].uuid,                
    #                     "attributes":{
    #                         "title": pipeline.title,                        
    #                         "field_id":pipeline.ID,
    #                         "field_author":pipeline.author,
    #                         "field_author_email":pipeline.author_email,
    #                         "body":pipeline.abstract,
    #                         "field_plugin_warnings":pipeline.plugin_warnings                            
    #                     }            
    #                 }
    #             }
                                
    #             r= self.HOST.patch(f"jsonapi/node/pipeline/{self.Pipelines[pipeline.ID].uuid}",payload)
    #             if(r.status_code!=200):                   
    #                 print(f"[ERROR] failed to patch pipeline {pipeline.ID} on CRUSH HOST: {r.status_code},  {r.reason}")
    #             else:                                     
    #                 if len(r.json()['data'])==0:
    #                     print("PipelineRepository::UpsertPipeline:  Pipeline not updated.")                
    #                 else:       
    #                     return r.json()['data']['id']
                    
    #             #Update



    #         else:
    #             print(f"PipelineRepository::New {pipeline.ID}, Inserting")
    #             #Insert
 
    #             payload = {"data" : {
    #                 "type":"node--pipeline",                    
    #                 "attributes":{
    #                     "field_author": pipeline.author, 
    #                     "title": pipeline.title,
    #                     "field_author_email":pipeline.author_email,
    #                     "body":pipeline.abstract,
    #                     "field_id":pipeline.ID
    #                 }               
    #             }}

    #             r= self.HOST.post("jsonapi/node/pipeline",payload)
    #             if(r.status_code!=201):
    #                 print(f"[ERROR] failed to create {ID} on CRUSH HOST: {r.status_code},  {r.reason}")
    #     except:
    #         if( not isinstance(pipeline,Pipeline)):
    #             print("Pipeline object not passed to upsert")
    #         else:
    #              traceback.print_exc()


