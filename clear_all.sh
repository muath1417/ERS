pip install -r requirements.txt
echo "" > db.sqlite3
find . -path "./Student/migrations/*.py" -not -name "__init__.py" -delete
find . -path "./Student/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  --username admin --email admin@localhost.com
python manage.py loaddata FileType.json
python manage.py loaddata Student.json
python manage.py loaddata Course.json