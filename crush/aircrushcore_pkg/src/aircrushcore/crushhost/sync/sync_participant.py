from aircrushcore.Models.Participant import Participant
from aircrushcore.Models.Session import Session
from aircrushcore.crushhost.dml.dml_participant import ParticipantRepository
from aircrushcore.crushhost.dml.dml_project import ProjectRepository
from aircrushcore.crushhost.dml.dml_session import SessionRepository
from aircrushcore.crushhost.crush import crush
import asyncio, asyncssh, sys
import requests
import json

#from aircrushcore import workflow
import importlib
import traceback
#import aircrushcore

def sync(host):
        
    crushHOST=None

    try:
        crushHOST=crush(
            endpoint="http://localhost:81/",
            username="crush",
            password="crush"
            )
    except:
        #traceback.print_exc()
        print("\n\n==========\nERROR: Unable to connect to crush host\n==========\n\n")
        return

    #For all projects that are published

    ProjectDict=ProjectRepository(host=crushHOST).getKnownProjects()
  
    for project in ProjectDict:
        print(f"{ProjectDict[project].title}, {project} {ProjectDict[project].field_username}")
        try:
            cmd='python3.8 ' + ProjectDict[project].field_path_to_crush_agent + '/project_status.py ' + ProjectDict[project].field_path_to_exam_data
            cmd='python3.8 ' + ProjectDict[project].field_path_to_crush_agent + '/ps2.py ' + ProjectDict[project].field_path_to_exam_data
            #cmd="python3.8 --version"
            print(cmd)
            
            asyncio.get_event_loop().run_until_complete(run_project_status_client(
                host=ProjectDict[project].field_host,
                username=ProjectDict[project].field_username,
                password=ProjectDict[project].field_password,                
                cmd=cmd,
                uuid=ProjectDict[project].uuid,
                crushHOST=host
            ))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SSH connection failed: ' + str(exc))


    # print
    #  try:
    #                 cmd='python ' + agentpath + '/project_status.py ' + examPath
    #                 print(cmd)
    #                 asyncio.get_event_loop().run_until_complete(run_project_status_client(
    #                     host=host,
    #                     username=username,
    #                     password=password,                
    #                     cmd=cmd,
    #                     uuid=uuid
    #                 ))
    #             except (OSError, asyncssh.Error) as exc:
    #                 sys.exit('SSH connection failed: ' + str(exc))


    #     for item in r.json()['data']:
    #         if(item['type']=='node--project'):
    #             uuid=item['id']            
    #             project=item['attributes']['title']
    #             host=item['attributes']['field_host']
    #             username=item['attributes']['field_username']
    #             password=item['attributes']['field_password']
    #             agentpath=item['attributes']['field_path_to_crush_agent']
    #             examPath=item['attributes']['field_path_to_exam_data']
    #             print(f'Connecting to {project:20s}')
               

   

async def run_project_status_client(host,username,password,cmd,uuid,crushHOST):
   # with open("/home/dmattie/.ssh/id_rsa","r") as mypkey:
   #     keydata=mypkey.readlines()
   # print(keydata)
    #print(f"host={host}, username={username},password={password},cmd={cmd},uuid={uuid}")

    async with asyncssh.connect(host,username=username, password=password, known_hosts=None) as conn:
        agentresult = await conn.run(cmd, check=True)
        print(f"Checking host {host} with command: {cmd}")
        project=uuid
        
        PR=ParticipantRepository(host=crushHOST,project=uuid)
        SR=SessionRepository(host=crushHOST,project=uuid)
        
        KnownParticipants=PR.getKnownParticipants()


        #for participant in PR.Participants:
        #    print(f"\t{PR.Participants[participant].title} / {PR.Participants[participant].field_project}")
        try:
            agentExams=json.loads(agentresult.stdout)
        except:
            print(agentresult)
            raise Exception("ERROR:sync_participant::Agent didn't return JSON")

        newnodes=0
        updatednodes=0
        for participant in agentExams['participants']: #Iterate exams in Project Directory
            #print(f"Syncing {participant}.")
            
            # if agentExams[participant]['isbids']=="True": 
            #     isbids="bids"
            # else:
            isbids="unknown"            

            participantExists=False
            for p in KnownParticipants:
                if participant==KnownParticipants[p].title:
                    participantExists=KnownParticipants[p].uuid
            
            if participantExists:#participant in KnownParticipants:
                #We've seen this participant before, update if different
                print("Participant Exists. Updating")
                metadata={
                    "title":agentExams['participants'][participant]['id'],
                    "isbids":isbids,
                    "field_project":project,
                    #"field_status":"",
                    "uuid":participantExists#KnownParticipants[participant].uuid
                }
                print(metadata)
                PR.upsertParticipant(Participant(metadata=metadata))
                
                updatednodes=updatednodes+1

                ##### Get sessions for participant
                KnownSessions=SR.getKnownSessions()
                
                #For this participant, iterate the sessions, and upsert
                for ses in agentExams['participants'][participant]['sessions']:
                    print( ses)

                    sessionExists=""
                    for kses in KnownSessions:
                        if ses==KnownSessions[kses].title:
                            sessionExists=KnownSessions[kses].uuid
                    
                    metadata={
                        "title":ses,
                        "field_participant":participantExists,
                        "field_status":"notstarted",
                        "uuid":sessionExists
                    }
                    SR.upsertSession(Session(metadata=metadata))
                #print(KnownSessions)

            else:
                #New participant, create
                metadata={
                    "title":agentExams['participants'][participant]['id'],
                    "isbids":isbids,
                    "field_project":project
                    #"field_status":"",
         
                }
                PR.upsertParticipant(Participant(metadata=metadata))
                newnodes=newnodes+1
                
            
        print(f"{newnodes} created, {updatednodes} updated.  The flux core is hot!")                                
                               

