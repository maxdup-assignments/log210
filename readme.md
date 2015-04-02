Log210
====
 
Installing the Rest server
====
* install python 2.7 ("sudo apt-get install python2")
* install pip2 ("sudo apt-get install pip2")
* install MongoDB
* if using virtualenv, "virtualenv env", ". env/bin/activate"

* install dependencies (pip install -r requirements.txt)

Running the REST server
====
move to log210/application
* "python2 manage.py runserver"

Installing the NodeJS app
====
* install nodejs
* in terminal (windows/linux) run:
⋅⋅⋅ "npm install -g grunt"
⋅⋅⋅ "npm install -g bower"
* move to the project root (this folder)
* run "npm install"
* compile coffescript files with "grunt coffee"
* to start the automatic coffee compiler, run the command "grunt"
* to start the nodejs server run "npm start"

