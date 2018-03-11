import datetime

from django.core.management.base import BaseCommand

from nalcs import util
from nalcs import models as nalcs_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        matches = nalcs_models.Match.objects.all()
        dates = set([match.date for match in matches])
        for date in sorted(dates):
            if date <= datetime.datetime.today().date():
                print("updating for {}".format(date))
                util.update_ratings_and_predictions(date)
