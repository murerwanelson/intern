import csv
import os
from django.core.management.base import BaseCommand
from zingsa_app.models import Person
from datetime import datetime
from django.conf import settings

class Command(BaseCommand):
    help = 'Import data from CSV file'

    def handle(self, *args, **kwargs):
        # Construct the path to the CSV file
        csv_file_path = os.path.join(settings.BASE_DIR, 'path_to_your_file', 'jan13.csv')

        try:
            with open(csv_file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    Person.objects.create(
                        department=row['Department'],
                        name=row['Name'],
                        number=int(row['No.']),
                        date_time=datetime.strptime(row['Date/Time'], '%d/%m/%Y %H:%M'),
                        location_id=int(row['Location ID']),
                        id_number=row['ID Number'],
                        verify_code=row['VerifyCode'],
                        card_no=row['CardNo']
                    )
            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {csv_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred: {str(e)}'))