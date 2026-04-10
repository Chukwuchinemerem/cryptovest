from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Creates a superuser if none exists (for Render deployment)'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                username='Admin2',
                email='Admin2@profitlynx.com',
                password='12345678'
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser created: username=Admin2 password=12345678'))
        else:
            self.stdout.write(self.style.WARNING('ℹ️  Superuser already exists — skipping.'))
