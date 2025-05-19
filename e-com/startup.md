# How to run program

##### Shows all commands available   
 ```bash 
 python ecom help
```
##### To initialize (for first-time setup on a new device)
 ```bash 
 python ecom init
```
##### Execute program 
 ```bash
 python ecom run
```
##### Makemigration program to check changes in models
 ```bash
 python ecom makemigrations
```
##### Migrate database make changes to database
 ```bash
 python ecom migrate
```
##### To install packages
 ```bash
 python ecom install {package_name}
```
##### To uninstall packages
 ```bash
 python ecom uninstall {package_name}
```
##### Returns list of installed  
 ```bash 
 python ecom list
```
##### Start new app   
 ```bash 
 python ecom startapp {app_name}
```

______________________________________________________________________________________________
##### TO CREATE VIRTUAL-ENVIRONMENT
```
pip install virtualenv
python -m venv {venv /*name of virtual environment*/}
```

##### To get all the dependencies in new environment
```
pip install -r requirements.txt
```
##### Update requirements.txt
```
pip freeze > requirements.txt
```

##### To start new project
```
django-admin startproject mysite djangotrial
```

##### run project
```
source venv/bin/activate  // for mac and linux
.\.venv\Scripts\activate  // for windows

cd e-com
python manage.py runserver
```
##### kill port
```
lsof -ti :{port}  // get pid
kill -9 {pid}     // kill port
```
