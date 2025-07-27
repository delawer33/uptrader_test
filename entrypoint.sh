#!/bin/sh

set -e

python manage.py migrate

python manage.py generate_menu_test_data

exec "$@"
