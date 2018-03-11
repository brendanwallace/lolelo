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

        season = models.Season.objects.get_or_create(
            name="Spring 2018",
            date=datetime.date(year=2018, month=1, date=20)
        )

        file_location = options['file']

        print("reading matches from {}".format(file_location))

        created = 0
        with open(file_location) as csv_file:
            match_reader = csv.reader(csv_file, delimiter=',')
            date = None # needs to get updated in the first loop
            week = None # needs to get updated in the first loop
            for row in match_reader:
                short_1 = row[0]
                short_2 = row[1]
                team1_wins = row[2]
                team2_wins = row[3]
                if len(row) >= 4:
                    date = datetime.strptime(row[4], '%Y-%m-%d').date()
                if len(row) >= 5:
                    week =  int(row[5])
                models.Match.objects.get_or_create(
                    team1=model.Team.objects.get(short=short_1),
                    team2=model.Team.objects.get(short=short_2),
                    date=date,
                    season=season,
                    team1_wins=team1_wins,
                    team2_wins=team2_wins,
                )
                created += 1

        print("success. got or created {} matches.".format(created))
