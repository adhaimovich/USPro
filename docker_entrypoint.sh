#!/usr/bin/env bash
#cd Preprocessing_backend

#python check_directories.py
#python manage.py makemigrations
#python manage.py makemigrations - we don't need this step...the migrate command will do it for us
python manage.py migrate
python manage.py collectstatic
python manage.py runserver 0.0.0.0:8000