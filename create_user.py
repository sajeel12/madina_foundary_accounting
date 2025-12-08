
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accounting_core.settings')
django.setup()

from django.contrib.auth.models import User

username = 'abdulwaheed'
password = 'abdulwaheed123'
email = 'abdulwaheed@example.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, email=email, password=password)
    print(f"User '{username}' created successfully.")
else:
    print(f"User '{username}' already exists.")
