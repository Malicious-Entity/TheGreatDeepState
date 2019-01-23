## Quick Start
Git clone, pip install -r requirements.txt  
Insert API keys for free or premium accounts in GreatDeepState/scripts: Shodan, Emailhunter, Censys  
Run GDS.py

## Docker version
To simplify requirements versions, and dependencies, a dockerized version was created. To get started, install Docker, and then build the image:

```
user@debian:~/$ sudo docker build -t gds  .
Sending build context to Docker daemon  316.4kB
Step 1/6 : FROM python:2.7
 ---> bd2db1324f76
Step 2/6 : WORKDIR /usr/src/app
 ---> Using cache
 ---> 6d08ec864eec
Step 3/6 : COPY requirements.txt ./
 ---> Using cache
 ---> 21e31f0192e5
Step 4/6 : RUN pip install --no-cache-dir -r requirements.txt
 ---> Using cache
 ---> 62170650580b
Step 5/6 : COPY . .
 ---> c1795006c51a
Step 6/6 : CMD python ./GreatDeepState/GDS.py
 ---> Running in c16ebde0b179
 ---> 015baabbcfd9
Removing intermediate container c16ebde0b179
Successfully built 015baabbcfd9
Successfully tagged GreatDeepState:latest
```

Once that is complete, you should be able to run from Docker. If you plan on exporting to files, it may be useful to create a temporary directory, and map it to the application directory for retrieval:

```
user@debian:~/$ mkdir tmp
user@debian:~/$ sudo docker run -it -v tmp:/usr/src/app gds

___________.__               ________                      __    ________                           _________ __          __          
\__    ___/|  |__   ____    /  _____/______   ____ _____ _/  |_  \______ \   ____   ____ ______    /   _____//  |______ _/  |_  ____  
  |    |   |  |  \_/ __ \  /   \  __\_  __ \_/ __ \\__  \\   __\  |    |  \_/ __ \_/ __ \\____ \   \_____  \\   __\__  \\   __\/ __ \ 
  |    |   |   Y  \  ___/  \    \_\  \  | \/\  ___/ / __ \|  |    |    `   \  ___/\  ___/|  |_> >  /        \|  |  / __ \|  | \  ___/ 
  |____|   |___|  /\___  >  \______  /__|    \___  >____  /__|   /_______  /\___  >\___  >   __/  /_______  /|__| (____  /__|  \___  >
                \/     \/          \/            \/     \/               \/     \/     \/|__|             \/           \/          \/ 

x========================================================================================================================================

Please Choose a Module:
 1. Email Hunter 
 2. DNSdumpster 
 3. Shodan 
 4. Censys 
 5. Github Org Search
 6. Github Single Repo Search 
 7. Github Search for Repos 
 8. All 
 9. Exit 

Module:

```
## To Add
Better output file control

## Issues
Zoomeye API was taken down, therefore it no longer works!

~~### Github modules not supported in windows~~
This seems to work now. ~~There's a function or two in truffleHog that only works on Unix.~~

### Github modules speeds
The Github module takes an extraordinarily long time to run against very large repos or organizations with a ton of repos. For example, Comcast has one repo with 22,000 commits. Searching through each one takes time. To get around this, there's an option to skip repos in an org search and also a module to search through single git repos if you want to let it run for awhile on a particularly large repo
Update: Added some performance improvements. Still need to figure out how to filter out checksum/versioning results that are getting picked up, but for now there's a hardcoded filter for strings starting with 'checksum' and some formatting filters

### Github modules won't graciously exit
Github module spawns a subprocess, using CTRL-C or CTRL+pause/break does not exit the subprocess properly. This manifests as the terminal you were working in becoming unresponsive. 

