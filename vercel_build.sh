#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

# Solo si usas django-tailwind
echo "Installing Tailwind CSS..."
python manage.py tailwind runserver

echo "Collecting static files..."
python manage.py collectstatic --noinput