import math
import datetime
import functools
import random

from nalcs import models as nalcs_models

from django.db import transaction

K_FACTOR = 20
LOGISTIC_PARAMETER = 400
INITIAL_RATING = 1500

SEASONS_TO_SIMULATE = 10000

MATCHES_ONLY = False

def expected_outcome(team_1_rating, team_2_rating):
    """
    Given two predictions' elo ratings, return the likelihood of the first winning.

    This is basically how elo ratings work, uses a logistic curve.
    """
    return 1 / (1 + math.pow(10, ((team_2_rating - team_1_rating) / LOGISTIC_PARAMETER)))

class SimulationTeam():
    """
    Utility class used to create a copy of a team for simulating the season.
    """
    def __init__(self, predictions):
        self.name = predictions.team.name
        self.rating = predictions.rating
        self.match_wins = predictions.match_wins
        self.game_wins = predictions.game_wins
        self.game_losses = predictions.game_losses
        # copying the dictionary...
        self.head_to_head = {a: b for a, b in predictions.head_to_head.items()}

    # for debugging
    def __str__(self):
        return self.name


def compare_simulation_team(a, b):# a: SimulationTeam, b: SimulationTeam) -> int: 
    """
    Orders predictions for end-of-season standings.

    Match wins first, then head to head between predictions, then game wins, then
    a single tie break game.
    """
    match_diff = a.match_wins - b.match_wins
    if match_diff != 0:
        return match_diff

    head_to_head = a.head_to_head[b.name] - b.head_to_head[b.name]
    if head_to_head != 0:
        return head_to_head

    game_diff = a.game_wins / (a.game_wins + a.game_losses) - b.game_wins / (b.game_wins + b.game_losses)
    if game_diff != 0:
        return game_diff

    # simulate a single game:
    a_win_p = 1 / (1 + math.pow(10, ((a.rating -b.rating) / LOGISTIC_PARAMETER)))
    if a_win_p >= random.random():
        return 1
    else:
        return -1


def simulate_match(
    team_1, team_2, first_to, predictions, adjust_records=True, adjust_ratings=True
):
    """
    Simulates team_1 playing team_2, adjusts records and ratings accordingly.

    Returns a tuple of (winning_team, losing_team).
    """
    team_1_win_p =  expected_outcome(team_1.rating, team_2.rating)

    # simulate the match:
    team_1_wins = 0
    team_2_wins = 0
    while team_1_wins < first_to and team_2_wins < first_to:
        if random.random() <= team_1_win_p:
            team_1_wins += 1
        else:
            team_2_wins += 1

    if adjust_records:
        team_1.game_wins += team_1_wins
        team_2.game_losses += team_1_wins
        team_2.game_wins += team_2_wins
        team_1.game_losses += team_2_wins

        if team_1_wins > team_2_wins:
            team_1.match_wins += 1
            team_1.head_to_head[team_2.name] += 1
        else:
            team_2.match_wins += 1
            team_2.head_to_head[team_1.name] += 1

    if adjust_ratings:
        games_played = team_1_wins + team_2_wins
        expected_team_1_wins = (
            expected_outcome(team_1.rating, team_2.rating) * games_played
        )
        expected_team_2_wins = (
            expected_outcome(team_2.rating, team_1.rating) * games_played
        )
        team_1.rating += K_FACTOR * (team_1_wins - expected_team_1_wins)
        team_2.rating += K_FACTOR * (team_2_wins - expected_team_2_wins)

    return (team_1, team_2) if team_1_wins > team_2_wins else (team_2, team_1)


@transaction.atomic
def update_ratings_and_predictions(date):
    """
    Updates ratings and predictions for a given date, meaning that it treats
    all completed matches after that date as unplayed.
    """
    # Hash by name so that predictions and prediction_copies can look into here. Also
    # to avoid an issue where modifying match.team_1 (for example) is modifying
    # a separate object.
    predictions = {}
    for team in nalcs_models.Team.objects.all():
        prediction, _ = nalcs_models.DailyPrediction.objects.get_or_create(team=team, date=date)
        predictions[team.name] = prediction

    spring_matches = nalcs_models.Match.objects.filter(season__name="Spring 2018").order_by('game_number')

    # reset ratings and everything:
    for _, pred in predictions.items():
        pred.rating = INITIAL_RATING
        pred.game_wins = 0
        pred.game_losses = 0
        pred.match_wins = 0
        pred.match_losses = 0
        # pred.championship_points = pred.team.spring_championship_points
        pred.head_to_head = {pred.team.name: 0 for _, pred in predictions.items()}

    # update the existing matches
    for match in [m for m in spring_matches if date >= m.date and m.finished]:
        team_1_expected_wins = (
            expected_outcome(predictions[match.team_1.name].rating, predictions[match.team_2.name].rating) *
            (match.team_1_wins + match.team_2_wins)
        )
        # should be the same as (res1 + res2) - team1_expected_wins
        team_2_expected_wins = (
            expected_outcome(predictions[match.team_2.name].rating, predictions[match.team_1.name].rating) *
            (match.team_1_wins + match.team_2_wins)
        )
        predictions[match.team_1.name].rating += K_FACTOR * (match.team_1_wins - team_1_expected_wins)
        predictions[match.team_2.name].rating += K_FACTOR * (match.team_2_wins - team_2_expected_wins)
        predictions[match.team_1.name].game_wins += match.team_1_wins
        predictions[match.team_1.name].game_losses += match.team_2_wins
        predictions[match.team_2.name].game_wins += match.team_2_wins
        predictions[match.team_2.name].game_losses += match.team_1_wins
        if match.team_1_wins > match.team_2_wins:
            predictions[match.team_1.name].match_wins += 1
            predictions[match.team_2.name].match_losses += 1
        else:
            predictions[match.team_2.name].match_wins += 1
            predictions[match.team_1.name].match_losses += 1

    for _, pred in predictions.items():
        pred.make_playoffs = 0.0
        pred.playoff_bye = 0.0
        pred.win_split = 0.0

    for _ in range(SEASONS_TO_SIMULATE):
        # set up data for this simulation
        simulation_teams = {
            prediction.team.name: SimulationTeam(prediction)
            for _, prediction in predictions.items()
        }

        # simulate the remaining spring split
        for match in [m for m in spring_matches if date < m.date or not m.finished]:
            simulate_match(simulation_teams[match.team_1.name], simulation_teams[match.team_2.name], 3, simulation_teams)

        # figure out who qualifies for playoffs:
        simulation_teams = [sim_team for _, sim_team in simulation_teams.items()]
        simulation_teams.sort(key=functools.cmp_to_key(compare_simulation_team), reverse=True)

        make_playoffs = simulation_teams[:6]
        playoff_bye = simulation_teams[:2]

        for sim_team in simulation_teams[:6]:
            predictions[sim_team.name].make_playoffs += 1

        for sim_team in simulation_teams[:2]:
            predictions[sim_team.name].playoff_bye += 1

        seed_1 = simulation_teams[0]
        seed_2 = simulation_teams[1]
        seed_3 = simulation_teams[2]
        seed_4 = simulation_teams[3]
        seed_5 = simulation_teams[4]
        seed_6 = simulation_teams[5]

        # quarter finals:
        quarter_4_w, finish_5_a = simulate_match(seed_4, seed_5, 3, predictions)
        quarter_3_w, finish_5_b = simulate_match(seed_3, seed_6, 3, predictions)

        # semis:
        semi_1_w, semi_1_l = simulate_match(seed_1, quarter_4_w, 3, predictions)
        semi_2_w, semi_2_l = simulate_match(seed_2, quarter_3_w, 3, predictions)

        # finals:
        finish_1, finish_2 = simulate_match(semi_1_w, semi_2_w, 3, predictions)

        # 3rd place consolation:
        finish_3, finish_4 = simulate_match(semi_1_l, semi_2_l, 3, predictions)

        predictions[finish_1.name].win_split += 1


    # # calculate the percentages from that:
    for _, prediction in predictions.items():
        prediction.make_playoffs = prediction.make_playoffs / SEASONS_TO_SIMULATE
        prediction.playoff_bye = prediction.playoff_bye / SEASONS_TO_SIMULATE
        prediction.win_split = prediction.win_split / SEASONS_TO_SIMULATE
        prediction.save()