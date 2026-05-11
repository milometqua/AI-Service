from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):
    help = 'Tạo tài khoản mẫu để demo'

    def handle(self, *args, **options):
        accounts = [
            {'username': 'admin',    'password': 'Admin@123',    'role': 'admin',    'email': 'admin@ecomai.vn',    'first_name': 'Admin'},
            {'username': 'staff01',  'password': 'Staff@123',    'role': 'staff',    'email': 'staff@ecomai.vn',    'first_name': 'Nhân viên'},
            {'username': 'customer', 'password': 'Customer@123', 'role': 'customer', 'email': 'customer@ecomai.vn', 'first_name': 'Khách hàng'},
        ]
        for acc in accounts:
            if not User.objects.filter(username=acc['username']).exists():
                User.objects.create_user(
                    username=acc['username'],
                    password=acc['password'],
                    email=acc['email'],
                    first_name=acc['first_name'],
                    role=acc['role'],
                )
                self.stdout.write(self.style.SUCCESS(f"✓ Created user: {acc['username']} / {acc['password']}"))
            else:
                self.stdout.write(f"  Skip: {acc['username']} already exists")
