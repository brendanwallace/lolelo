"""
This is kind of a quick fix to avoid having to reenter data.
"""
import datetime
import math

from django.core.management.base import BaseCommand

from nalcs import models as nalcs_models

from django.db import transaction


K_FACTOR = 20
LOGISTIC_PARAMETER = 400
INITIAL_RATING = 1500

MATCHES_ONLY = False

def expected_outcome(team_1_snalcs, team_2_snalcs):
  return 1 / (1 + math.pow(10, ((team_2_snalcs- team_1_snalcs) / LOGISTIC_PARAMETER)))

class Command(BaseCommand):
    def handle(self, *args, **options):
        setup()

@transaction.atomic
def setup():
    C9, _ = nalcs_models.Team.objects.get_or_create(name="Cloud9", spring_championship_points=70)
    CLG, _ = nalcs_models.Team.objects.get_or_create(name="Counter Logic Gaming", spring_championship_points=10)
    IMT, _ = nalcs_models.Team.objects.get_or_create(name="Immortals")
    DIG, _ = nalcs_models.Team.objects.get_or_create(name="Team Dignitas", spring_championship_points=10)
    TSM, _ = nalcs_models.Team.objects.get_or_create(name="Team SoloMid", spring_championship_points=90)
    nV, _ = nalcs_models.Team.objects.get_or_create(name="Team Envy")
    FOX, _ = nalcs_models.Team.objects.get_or_create(name="Echo Fox")
    TL, _ = nalcs_models.Team.objects.get_or_create(name="Team Liquid")
    FLY, _ = nalcs_models.Team.objects.get_or_create(name="Flyquest", spring_championship_points=30)
    P1, _ = nalcs_models.Team.objects.get_or_create(name="Phoenix 1", spring_championship_points=50)

    teams = [C9, CLG, IMT, DIG, TSM, nV, FOX, TL, FLY, P1]

    spring_2017_results = [
        [
            (TSM, C9, 0, 2),
            (FOX, P1, 0, 2),
            (CLG, TL, 0, 2),
            (nV, FLY, 0, 2),
            (FOX, IMT, 1, 2),
            (DIG, P1, 2, 1),
            (TSM, IMT, 2, 1),
            (nV, CLG, 0, 2),
            (DIG, C9, 1, 2),
            (TL, FLY, 1, 2),
        ],
        [
            (FLY, CLG, 2, 0),
            (TSM, DIG, 2, 1),
            (IMT, C9, 0, 2),
            (P1, nV, 2, 0),
            (TSM, TL, 2, 1),
            (DIG, FOX, 1, 2),
            (P1, TL, 2, 0),
            (FOX, FLY, 2, 1),
            (nV, IMT, 1, 2),
            (C9, CLG, 2, 1),
        ],
        [
            (IMT, P1, 0, 2),
            (nV, TL, 2, 0),
            (CLG, TSM, 1, 2),
            (FLY, DIG, 2, 0),
            (TL, FOX, 2, 1),
            (C9, nV, 2, 0),
            (P1, TSM, 1, 2),
            (DIG, CLG, 0, 2),
            (IMT, FLY, 0, 2),
            (C9, FOX, 2, 0),
        ],
        [
            (C9, TL, 2, 1),
            (IMT, DIG, 2, 0),
            (CLG, FOX, 0, 2),
            (P1, FLY, 0, 2),
            (TSM, nV, 2, 0),
            (TL, IMT, 0, 2),
            (FOX, TSM, 2, 0),
            (CLG, P1, 2, 1),
            (DIG, nV, 2, 0),
            (FLY, C9, 1, 2),
        ],
        [
            (DIG, FLY, 2, 0),
            (nV, P1, 0, 2),
            (CLG, IMT, 2, 1),
            (TL, DIG, 1, 2),
            (C9, TSM, 1, 2),
            (nV, FOX, 2, 0),
            (FLY, TSM, 1, 2),
            (IMT, FOX, 2, 0),
            (P1, C9, 2, 0),
            (TL, CLG, 1, 2),
        ],
        [
            (IMT, TL, 1, 2),
            (P1, CLG, 1, 2),
            (FOX, C9, 0, 2),
            (FLY, nV, 2, 1),
            (TSM, CLG, 2, 0),
            (P1, DIG, 2, 1),
            (DIG, TSM, 0, 2),
            (FOX, TL, 2, 1),
            (C9, FLY, 2, 0),
            (IMT, nV, 1, 2),
        ],
        [
            (TL, C9, 0, 2),
            (FLY, P1, 0, 2),
            (CLG, DIG, 0, 2),
            (nV, TSM, 1, 2),
            (FLY, IMT, 0, 2),
            (P1, FOX, 2, 0),
            (CLG, C9, 2, 1),
            (FOX, DIG, 1, 2),
            (IMT, TSM, 1, 2),
            (TL, nV, 2, 1),
        ],
        [
            (DIG, TL, 2, 0),
            (FOX, CLG, 0, 2),
            (C9, IMT, 1, 2),
            (nV, DIG, 1, 2),
            (TSM, FLY, 2, 1),
            (TL, P1, 0, 2),
            (TSM, FOX, 2, 0),
            (P1, IMT, 2, 0),
            (CLG, FLY, 2, 0),
            (nV, C9, 1, 2),
        ],
        [
            (C9, DIG, 2, 0),
            (FLY, FOX, 2, 0),
            (IMT, CLG, 2, 0),
            (TL, TSM, 2, 1),
            (C9, P1, 2, 0),
            (FOX, nV, 2, 1),
            (TSM, P1, 2, 0),
            (DIG, IMT, 2, 0),
            (FLY, TL, 2, 1),
            (CLG, nV, 2, 1),
        ],
        # playoffs
        [],
    ]

    summer_2017_results = [
        [
            (C9, CLG, 1, 2),
            (IMT, P1, 2, 1),
            (CLG, TL, 2, 0),
            (FOX, FLY, 2, 0),
            (TSM, C9, 2, 0),
            (DIG, nV, 2, 1),
            (IMT, TSM, 2, 0),
            (nV, P1, 2, 0),
            (FLY, DIG, 0, 2),
            (TL, FOX, 0, 2),
        ],
        [
            (P1, C9, 0, 2),
            (IMT, nV, 0, 2),
            (DIG, TSM, 2, 1),
            (FOX, CLG, 1, 2),
            (IMT, FLY, 2, 1),
            (nV, TL, 2, 1),
            (FOX, C9, 0, 2),
            (DIG, TL, 1, 2),
            (CLG, TSM, 1, 2),
            (P1, FLY, 0, 2),
        ],
        [
            (IMT, TL, 2, 0),
            (nV, FOX, 0, 2),
            (TL, TSM, 0, 2),
            (IMT, C9, 2, 1),
            (FLY, CLG, 1, 2),
            (P1, DIG, 1, 2),
            (nV, TSM, 0, 2),
            (P1, CLG, 1, 2),
            (FLY, C9, 0, 2),
            (DIG, FOX, 2, 1),
        ],
        [
            (IMT, CLG, 2, 0),
            (FOX, P1, 0, 2),
            (TSM, FLY, 2, 0),
            (CLG, nV, 2, 1),
            (C9, TL, 2, 0),
            (IMT, DIG, 2, 1),
            (TSM, FOX, 2, 0),
            (TL, P1, 2, 1),
            (C9, DIG, 2, 1),
            (FLY, nV, 1, 2),
        ],
        [
            (C9, TSM, 2, 1),
            (P1, nV, 2, 1),
            (TSM, IMT, 2, 0),
            (CLG, C9, 2, 1),
            (DIG, FLY, 1, 2),
            (FOX, TL, 2, 1),
            (P1, IMT, 2, 1),
            (FLY, FOX, 2, 1),
            (nV, DIG, 2, 1),
            (TL, CLG, 0, 2),
        ],
        [
            (CLG, FLY, 2, 0),
            (IMT, FOX, 2, 0),
            (TSM, P1, 0, 0),
            (CLG, DIG, 0, 0),
            (C9, nV, 0, 0),
            (TL, FLY, 0, 0),
            (C9, IMT, 0, 0),
            (DIG, P1, 0, 0),
            (TSM, TL, 0, 0),
            (FOX, nV, 0, 0), 
        ],
        [
            (C9, P1, 0, 0),
            (TL, nV, 0, 0),
            (TSM, DIG, 0, 0),
            (CLG, FOX, 0, 0),
            (FLY, IMT, 0, 0),
            (P1, TL, 0, 0),
            (DIG, C9, 0, 0),
            (FOX, TSM, 0, 0),
            (CLG, IMT, 0, 0),
            (nV, FLY, 0, 0),
        ],
        [
            (P1, FOX, 0, 0),
            (TL, IMT, 0, 0),
            (FLY, TSM, 0, 0),
            (nV, CLG, 0, 0),
            (DIG, IMT, 0, 0),
            (TL, C9, 0, 0),
            (C9, FLY, 0, 0),
            (CLG, P1, 0, 0),
            (TSM, nV, 0, 0),
            (FOX, DIG, 0, 0),
        ],
        [
            (nV, IMT, 0, 0),
            (DIG, CLG, 0, 0),
            (P1, TSM, 0, 0),
            (nV, C9, 0, 0),
            (FOX, IMT, 0, 0),
            (FLY, TL, 0, 0),
            (C9, FOX, 0, 0),
            (TL, DIG, 0, 0),
            (TSM, CLG, 0, 0),
            (FLY, P1, 0, 0),
        ],
    ]

    spring_2017, _ = nalcs_models.Season.objects.get_or_create(
        date=datetime.date(2017, 1, 1), name="Spring 2017")
    summer_2017, _ = nalcs_models.Season.objects.get_or_create(
        date=datetime.date(2017, 6, 1), name="Summer 2017")

    for season, results in [
        (spring_2017, spring_2017_results), (summer_2017, summer_2017_results)
    ]:
        game_number = 1
        for week_index, week in enumerate(results):
            for team_1, team_2, wins_1, wins_2 in week:

                match, _ = nalcs_models.Match.objects.get_or_create(
                    team_1=team_1, team_2=team_2, week=(week_index + 1), best_of=3,
                    season=season, game_number=game_number
                )
                match.team_1_wins = wins_1
                match.team_2_wins = wins_2
                match.save()
                game_number += 1
