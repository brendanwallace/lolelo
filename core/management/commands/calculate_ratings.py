import datetime
import math

from django.core.management.base import BaseCommand

from core import models as core_models


K_FACTOR = 20
LOGISTIC_PARAMETER = 400
INITIAL_RATING = 1500

MATCHES_ONLY = False

def expected_outcome(team_1_score, team_2_score):
  return 1 / (1 + math.pow(10, ((team_2_score- team_1_score) / LOGISTIC_PARAMETER)))

class Command(BaseCommand):
    def handle(self, *args, **options):
        calculate_ratings()

def calculate_ratings():
    teams = {
        team: team
        for team in core_models.Team.objects.all()
    }
    spring_matches = core_models.Match.objects.filter(season__name="Spring 2017").order_by('game_number')
    for match in spring_matches:
        if match.team_1_wins + match.team_2_wins > 0:
            team_1_expected_score = (
                expected_outcome(teams[match.team_1].rating, teams[match.team_2].rating) *
                (match.team_1_wins + match.team_2_wins)
            )
            # should be the same as (res1 + res2) - team1_expected_score
            team_2_expected_score = (
                expected_outcome(teams[match.team_2].rating, teams[match.team_1].rating) *
                (match.team_1_wins + match.team_2_wins)
            )
            teams[match.team_1].rating += K_FACTOR * (match.team_1_wins - team_1_expected_score)
            teams[match.team_2].rating += K_FACTOR * (match.team_2_wins - team_2_expected_score)

    # regress 50%
    for team in teams:
        team.rating = 0.5 * INITIAL_RATING + 0.5 * team.rating

    # calculate summer ratings:
    summer_matches = core_models.Match.objects.filter(season__name="Summer 2017").order_by('game_number')

    # other summer stuff:
    for match in summer_matches:
        if match.team_1_wins + match.team_2_wins > 0:
            teams[match.team_1].game_wins += match.team_1_wins
            teams[match.team_1].game_losses += match.team_2_wins
            teams[match.team_2].game_wins += match.team_2_wins
            teams[match.team_2].game_losses += match.team_1_wins
            if match.team_1_wins >= 2 or match.team_2_wins >= 2:
                if match.team_1_wins > match.team_2_wins:
                    teams[match.team_1].match_wins += 1
                    teams[match.team_2].match_losses += 1
                else:
                    teams[match.team_2].match_wins += 1
                    teams[match.team_1].match_losses += 1
            team_1_expected_score = (
            expected_outcome(teams[match.team_1].rating, teams[match.team_2].rating) *
                (match.team_1_wins + match.team_2_wins)
            )
            # should be the same as (res1 + res2) - team1_expected_score
            team_2_expected_score = (
                expected_outcome(teams[match.team_2].rating, teams[match.team_1].rating) *
                (match.team_1_wins + match.team_2_wins)
            )
            teams[match.team_1].rating += K_FACTOR * (match.team_1_wins - team_1_expected_score)
            teams[match.team_2].rating += K_FACTOR * (match.team_2_wins - team_2_expected_score)

    for _, team in teams.items():
        team.save()

