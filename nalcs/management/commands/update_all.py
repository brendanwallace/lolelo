from datetime import datetime

from django.core.management.base import BaseCommand

from nalcs import util
from nalcs import models as nalcs_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        for date in sorted(list({match.date for match in nalcs_models.Match.objects.all().order_by('date')})): # if match.date <= datetime.today().date()
            print("updating for {}...".format(date))
            util.update_ratings_and_predictions(date)
