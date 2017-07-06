from django.core.management.base import BaseCommand

from core import util

def expected_outcome(team_1_score, team_2_score):
  return 1 / (1 + math.pow(10, ((team_2_score- team_1_score) / LOGISTIC_PARAMETER)))

class Command(BaseCommand):
    def handle(self, *args, **options):
        util.predict_season()
