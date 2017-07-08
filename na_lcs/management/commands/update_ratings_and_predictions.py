from django.core.management.base import BaseCommand

from na_lcs import util

class Command(BaseCommand):
    def handle(self, *args, **options):
        util.update_ratings_and_predictions()
