import math
import datetime
import functools
import random

from core import models as core_models

K_FACTOR = 20
LOGISTIC_PARAMETER = 400
INITIAL_RATING = 1500

SEASONS_TO_SIMULATE = 10000

MATCHES_ONLY = False


def expected_outcome(team_1_score, team_2_score):
  return 1 / (1 + math.pow(10, ((team_2_score- team_1_score) / LOGISTIC_PARAMETER)))

def calculate_ratings():
    teams = {
        team: team
        for team in core_models.Team.objects.all()
    }
    # reset ratings and everything:
    for team in teams:
        team.rating = INITIAL_RATING
        team.game_wins = 0
        team.game_losses = 0
        team.match_wins = 0
        team.match_losses = 0

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


class TeamCopy():
    def __init__(self, team):
        self.name = team.name
        self.rating = team.rating
        self.match_wins = team.match_wins
        self.game_wins = team.game_wins
        self.game_losses = team.game_losses
        self.championship_points = team.championship_points
        # copying the dictionary...
        self.head_to_head = {a: b for a, b in team.head_to_head.items()}

def compare_team_copy(a, b):
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

# returns winner, loser
def simulate_match(team_1, team_2, first_to, teams, adjust_records=True, adjust_ratings=True):

    team_1_win_p =  1 / (1 + math.pow(10, ((team_2.rating - team_1.rating) / LOGISTIC_PARAMETER)))

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

    # adjust ratings:
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

def predict_season():
    # matches played and unplayed (to record head-to-head for tie breaks)
    summer_matches = core_models.Match.objects.filter(season__name="Summer 2017").order_by('game_number')

    # initial teams
    teams = {team.name: team for team in core_models.Team.objects.all()}
    for _, team in teams.items():
        team.head_to_head = {team.name: 0 for _, team in teams.items()}
        team.make_playoffs = 0.0
        team.playoff_bye = 0.0
        team.win_split = 0.0
        team.qualify_for_worlds = 0.0

    # initialize the head-to-head:
    for match in summer_matches:
        if match.team_1_wins + match.team_2_wins == 0:
            continue
        if match.team_1_wins > match.team_2_wins:
            teams[match.team_1.name].head_to_head[match.team_2.name] += 1
        else:
            teams[match.team_2.name].head_to_head[match.team_1.name] += 1

    for _ in range(SEASONS_TO_SIMULATE):
        # set up data for this simulation
        team_copies = {
            team.name: TeamCopy(team)
            for _, team in teams.items()
        }

        # simulate the remaining summer split
        for match in summer_matches:
            if match.team_1_wins + match.team_2_wins > 0:
                continue
            simulate_match(team_copies[match.team_1.name], team_copies[match.team_2.name], 3, team_copies)

        # figure out who qualifies for playoffs:
        team_copies = [team_copy for _, team_copy in team_copies.items()]
        team_copies.sort(key=functools.cmp_to_key(compare_team_copy), reverse=True)

        make_playoffs = team_copies[:6]
        playoff_bye = team_copies[:2]

        for team_copy in team_copies[:6]:
            teams[team_copy.name].make_playoffs += 1

        for team_copy in team_copies[:2]:
            teams[team_copy.name].playoff_bye += 1

        seed_1 = team_copies[0]
        seed_2 = team_copies[1]
        seed_3 = team_copies[2]
        seed_4 = team_copies[3]
        seed_5 = team_copies[4]
        seed_6 = team_copies[5]

        quarter_4_w, finish_5_a = simulate_match(seed_4, seed_5, 3, teams)
        quarter_3_w, finish_5_b = simulate_match(seed_3, seed_6, 3, teams)
        semi_1_w, semi_1_l = simulate_match(seed_1, quarter_4_w, 3, teams)
        semi_2_w, semi_2_l = simulate_match(seed_2, quarter_3_w, 3, teams)
        finish_1, finish_2 = simulate_match(semi_1_w, semi_2_w, 3, teams)
        finish_3, finish_4 = simulate_match(semi_1_l, semi_2_l, 3, teams)

        teams[finish_1.name].win_split += 1
        teams[finish_1.name].qualify_for_worlds += 1

        finish_2.championship_points += 90
        finish_3.championship_points += 70
        finish_4.championship_points += 40
        finish_5_a.championship_points += 20
        finish_5_b.championship_points += 20

        # print(finish_1.name)

        team_copies.remove(finish_1)
        team_copies.sort(key=lambda team_copy: team_copy.championship_points, reverse=True)
        teams[team_copies[0].name].qualify_for_worlds += 1
        # for team_copy in team_copies:
        #     print("{} {}".format(team_copy.name, team_copy.championship_points))

    # calculate the percentages from that:
    for _, team in teams.items():
        team.make_playoffs = team.make_playoffs / SEASONS_TO_SIMULATE
        team.playoff_bye = team.playoff_bye / SEASONS_TO_SIMULATE
        team.win_split = team.win_split / SEASONS_TO_SIMULATE
        team.qualify_for_worlds = team.qualify_for_worlds / SEASONS_TO_SIMULATE
        team.save()



