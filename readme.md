Log210
====
 
Installation
====
install python 2.7 ("sudo apt-get install python2")
install pip2 ("sudo apt-get install pip2")

if using virtualenv
    "virtualenv env"
    ". env/bin/activate"

install dependencies (pip install -r requirements.txt)

Running the server
====
move to log210/application
"python2 manage.py runserver"

Installing js coffeescript compiler
====
-install nodejs
in terminal (windows/linux) run: "npm install -g grunt"
-move to the project root (this folder)
-run "npm install"
-compile coffescript files with the command "grunt coffee"

to start the automatic coffee compiler, run the command "grunt"

Dev Process
====
AGILE board https://trello.com/b/2cF77Xnl/log210

