from django.core.management.base import BaseCommand

from na_lcs import util

def expected_outcome(team_1_sna_lcs, team_2_sna_lcs):
  return 1 / (1 + math.pow(10, ((team_2_sna_lcs- team_1_sna_lcs) / LOGISTIC_PARAMETER)))

class Command(BaseCommand):
    def handle(self, *args, **options):
        util.calculate_ratings()
