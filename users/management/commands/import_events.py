import csv
from django.core.management.base import BaseCommand
from users.models import Event
import os

class Command(BaseCommand):
    help = 'Imports events from a specified CSV file into the database, overwriting existing records.'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='Path to the CSV file to import events from.',
            nargs='?',
            default='/Users/harrisdhanraj/Event-Recommendation-System/Event-Recommendation-System/events_detail.csv'
        )

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        if not os.path.exists(csv_file):
            self.stderr.write(self.style.ERROR(f"File not found: {csv_file}"))
            return

        try:
            with open(csv_file, newline='', encoding='utf-8', errors='ignore') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    event, created = Event.objects.update_or_create(
                        event_tag=row['event_tag'],
                        event_name=row['event_name'],
                        defaults={
                            'date': row['date'],
                            'time': row['time'],
                            'image_url': row['image_url'],
                            'city': row['city'],
                            'location': row['location'],
                            'description': row['description'],
                            'booking_url': row['booking_url'],
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Successfully added new event: {row["event_name"]}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Successfully updated event: {row["event_name"]}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred: {str(e)}"))
