# E-commerce

E-commerce is an internship project at [SARY](https://sary.com/)

## How To Run This Project?

1- clone this repo 
```bash
git clone https://github.com/mofahmi99/e_commerce.git
```
2- create virtual env 
```bash
sudo apt-get install python3-venv    # If needed
python3 -m venv env
```
3-activate virtiual env
```bash  
source env/bin/activate
```
4-install requirements 
``` bash
pip install -r requirements.txt
```
5- create conf.ini file in project main directory 
```bash
it should contains these data:

[global]
DEBUG : True
TEST : True

[database]
DB_NAME : your_db_name
DB_USER : your_db_user
DB_PASSWORD : your_db_password
DB_HOST : your_db_host
DB_PORT : your_db_port

[email]
USER : your_email
PASSWORD : your_email_password
```
6- run this command 
``` bash
python manage.py makemigrations 
```

7 - run this command
```bash
python manage.py migrate 
```
8- run this command
```bash
python manage.py createsuperuser
```
9- run this command
```bash
python manage.py runserver
```
## Notes

Project database schema [here](https://fv2-3.failiem.lv/down.php?i=b5d7f23tf&view) 

