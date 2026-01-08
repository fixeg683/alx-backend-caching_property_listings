from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json

class Command(BaseCommand):
    help = 'Setup periodic task for CRM report generation'

    def handle(self, *args, **options):
        # Create a schedule to run daily at 2:00 AM
        schedule, _ = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='2',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        # Create the periodic task
        PeriodicTask.objects.get_or_create(
            crontab=schedule,
            name='Generate CRM Report Daily',
            task='crm.tasks.generate_crm_report',
            defaults={
                'enabled': True,
                'one_off': False,
            }
        )
        
        self.stdout.write(self.style.SUCCESS('Successfully setup periodic task for CRM report'))