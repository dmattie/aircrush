import crushhost 

crush=crushhost.crush(endpoint="http://localhost:81/",username="crush",password="crush")

print (crush.connection.endpoint)
