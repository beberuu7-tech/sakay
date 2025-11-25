from django.core.management.base import BaseCommand
from django.core.management import call_command
from myapp.models import Route
import os

class Command(BaseCommand):
    help = 'Load initial data only if database is empty'

    def handle(self, *args, **kwargs):
        # Check if data already exists
        if Route.objects.exists():
            self.stdout.write(self.style.WARNING('⚠ Data already exists. Skipping load.'))
            return

        # Load the fixture
        fixture_path = 'db_data.json'
        if not os.path.exists(fixture_path):
            self.stdout.write(self.style.ERROR(f'❌ Fixture file not found: {fixture_path}'))
            return

        try:
            self.stdout.write(self.style.SUCCESS('📦 Loading initial data...'))
            call_command('loaddata', fixture_path, verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Data loaded successfully!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error loading data: {str(e)}'))
            # Don't fail the build, just log the error
            self.stdout.write(self.style.WARNING('⚠ Continuing without initial data...'))