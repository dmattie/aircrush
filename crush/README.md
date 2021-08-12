## DOING

Make HCPSlurmJob operator work
 - need a task type  
   - - taks will string together operators
   - - operators each have a log, tasks need to have multiple log support, or consolidate maybe use comment

## TODO

https://www.danielmorell.com/blog/dynamically-calling-functions-in-python-safely


Singularity container:  Thanks! It took a little tweaking from the docker version they provided, but the singularity container works fine! If you run into any bugs setting one up, feel free to give me a shout (pcamach2@illinois.edu)


Createing tasks in heartbeat:  payload in reository malformed, parameters is dict and pipeline isn't guid

Had to run this after using drush:  sudo docker exec 66c3bc9e233c composer require drush/drush

# Commands to remember
sudo docker container ls
sudo docker exec 64e7629403f2 drush user-information admin
