import datetime
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
        season_start = datetime.date(2018, 1, 20)

        season, created = models.Season.objects.get_or_create(
            name="Spring 2018",
            date=season_start
        )

        file_location = options['file']

        print("reading matches from {}".format(file_location))

        created = 0
        game_number = 0
        with open(file_location) as csv_file:
            game_number += 1
            match_reader = csv.reader(csv_file, delimiter=',')
            date = None # needs to get updated in the first loop
            week = None # needs to get updated in the first loop
            for row in match_reader:
                print("creating for " + str(row))
                short_1 = row[0]
                short_2 = row[1]
                team_1_wins = int(row[2])
                team_2_wins = int(row[3])
                if len(row) >= 5:
                    date = datetime.datetime.strptime(row[4], '%Y/%m/%d').date()
                if len(row) >= 6:
                    week =  int(row[5])
                match, _ = models.Match.objects.get_or_create(
                    team_1=models.Team.objects.get(short=short_1),
                    team_2=models.Team.objects.get(short=short_2),
                    date=date,
                    season=season,
                    week=week,
                    game_number=game_number
                )
                match.team_1_wins=team_1_wins
                match.team_2_wins=team_2_wins
                match.save()
                created += 1

        print("success. got or created {} matches.".format(created))
