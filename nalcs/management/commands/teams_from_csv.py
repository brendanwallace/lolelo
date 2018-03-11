from datetime import datetime
import csv

from django.core.management.base import BaseCommand

from nalcs import models

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            dest='file',
        )

    def handle(self, *args, **options):
        file_location = options['file']

        print("reading teams from {}".format(file_location))

        created = 0
        with open(file_location) as csv_file:
            team_reader = csv.reader(csv_file, delimiter=',')
            for row in team_reader:
                name = row[0]
                short = row[1]
                models.Team.objects.get_or_create(name=name, short=short)
                created += 1

        print("success. got or created {} teams.".format(created))