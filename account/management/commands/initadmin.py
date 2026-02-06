import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = "Creates a superuser using email only if it doesn't exist"

    def handle(self, *args, **options):
        # 1. Get credentials from Environment Variables
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not email or not password:
            self.stdout.write("No superuser credentials found in environment. Skipping.")
            return

        # 2. Check if user exists
        if not User.objects.filter(email=email).exists():
            self.stdout.write(f"Creating superuser: {email}")

            # 3. Create the superuser (email-only)
            User.objects.create_superuser(
                email=email,
                password=password
            )

            self.stdout.write(self.style.SUCCESS("Superuser created successfully!"))
        else:
            self.stdout.write("Superuser already exists. Skipping.")
