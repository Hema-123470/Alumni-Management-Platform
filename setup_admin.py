"""
Quick script to create an admin user after running migrations.
Usage: python setup_admin.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_management.settings')
django.setup()

from accounts.models import CustomUser


def create_admin():
    print("=== Create Admin User ===\n")

    email = input("Email: ").strip()
    username = input("Username: ").strip()
    first_name = input("First Name: ").strip()
    last_name = input("Last Name: ").strip()
    password = input("Password: ").strip()

    if CustomUser.objects.filter(email=email).exists():
        print(f"\n❌ User with email {email} already exists.")
        return

    user = CustomUser.objects.create_user(
        email=email,
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        role=CustomUser.Role.ADMIN,
        is_approved=True,
        is_staff=True,
        is_superuser=True,
    )

    print(f"\n✅ Admin user '{user.email}' created successfully!")
    print(f"   Role: {user.role}")
    print(f"   Approved: {user.is_approved}")
    print(f"\nYou can now log in at http://127.0.0.1:8000/login/")


if __name__ == '__main__':
    create_admin()
