#!/usr/bin/env bash
set -e

echo "Installing dependencies..."
python -m pip install --break-system-packages -r requirements.txt

echo "Installing Tailwind CSS..."
python manage.py tailwind build --force

echo "Collecting static files..."
python manage.py collectstatic --noinput