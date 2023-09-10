# tvk
curent internal control

This app tested python 3.10

To run this app:
+ install python3, pip3, python3-venv
+ copy this project 
+ cd project/dj
+ python3 -m venv venv
+ source venv/bin/activate (activate virtual enviroment)
+ pip3 install -r requirements.txt (install dependencies)
+ ./manage.py migrate (apply migrations for DB, if you need)
+ ./manage.py loaddata fixture/department.json (if you run at first)
+ ./manage.py loaddata fixture/imns.json (if you run at first)
+ ./manage.py loaddata fixture/user.json (if you run at first)
+ ./manage.py runsever {ip:port} (start app)