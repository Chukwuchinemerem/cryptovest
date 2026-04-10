from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Process daily profits for all active investments'

    def handle(self, *args, **options):
        from dashboard.utils import process_daily_profits
        self.stdout.write('Processing daily profits...')
        process_daily_profits()
        self.stdout.write(self.style.SUCCESS('✅ Daily profits processed.'))
