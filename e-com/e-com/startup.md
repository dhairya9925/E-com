## TO CREATE VIRTUAL-ENVIRONMENT
pip install virtualenv
python -m venv {venv /*name of virtual environment*/}


## TO GET ALL THE DEPENDENCIES IN NEW ENVIRONMENT
pip install -r requirements.txt

# -- update requirements.txt
pip freeze > requirements.txt


## TO START PROJECT ##
django-admin startproject mysite djangotrial

# -- run projector
source venv/bin/activate  // for mac and linux

.\.venv\Scripts\activate  // for windows
cd e-com
python manage.py runserver

# -- kill port
lsof -ti :{port}  // get pid
kill -9 {pid}     // kill port

