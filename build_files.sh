#!/bin/bash

echo "===== BUILD START ====="

echo "===== Installing dependencies ====="
pip install --upgrade pip
pip install -r requirements.txt

echo "===== Collecting static files ====="
python3 manage.py collectstatic --noinput --clear

echo "===== Running migrations ====="
python3 manage.py migrate --noinput

echo "===== BUILD END ====="