#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install libraries
pip install -r requirements.txt

# Convert static files
python manage.py collectstatic --no-input

