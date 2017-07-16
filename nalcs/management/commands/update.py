from datetime import datetime

from django.core.management.base import BaseCommand

from nalcs import util

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            dest='date',
            type=lambda s: datetime.strptime(s, '%Y-%m-%d').date(),
            default=datetime.today().date()
        )

    def handle(self, *args, **options):
        print("updating for {}".format(options['date']))
        util.update_ratings_and_predictions(options['date'])
