#!/usr/bin/env bash
set -o errexit

echo "--- Installing Dependencies ---"
pip install -r requirements.txt

echo "--- Collecting Static Files ---"
python manage.py collectstatic --no-input --clear

echo "--- Running Database Migrations (for session framework) ---"
python manage.py migrate

echo "--- Build Finished ---"
