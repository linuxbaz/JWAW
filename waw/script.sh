#!/bin/bash

systemctl start mysql
python manage.py runserver
