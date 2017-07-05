import math

from django import http
from django import shortcuts

from core import models as core_models
from core import hard_coded

LOGISTIC_PARAMETER = 400

def add_match_predictions(match):
    w1 =  1 / (1 + math.pow(10, ((match.team_2.rating- match.team_1.rating) / LOGISTIC_PARAMETER)))
    w2 = 1 - w1

    match.p_2_0 = w1 * w1
    match.p_0_2 = w2 * w2

    match.p_2_1 = w1*w2*w1 + w2*w1*w1
    match.p_1_2 = w2*w1*w2 + w1*w2*w2

    match.team_1_win_p = '{0:.0f}%'.format(100 * (match.p_2_0 + match.p_2_1))
    match.team_2_win_p = '{0:.0f}%'.format(100 * (match.p_0_2 + match.p_1_2))


def index(request):
    # teams:
    teams = core_models.Team.objects.all().order_by('-rating')
    for team in teams:
        team.rating = '{0:.0f}'.format(team.rating)
        team.make_playoffs = '65%'
        team.win_split = '10%'
        team.qualify_for_worlds = '15%'

    # matches:
    match_predictions_by_week = []
    week = None
    matches = None
    for match in core_models.Match.objects.filter(team_1_wins=0).filter(team_2_wins=0).order_by('game_number'):
        add_match_predictions(match)
        if week != match.week:
            week = match.week
            matches = []
            match_predictions_by_week.append({'title': 'week {}'.format(week), 'matches': matches})
        matches.append(match)


    context = {
        'teams': teams,
        'match_predictions_by_week': match_predictions_by_week
    }
    return shortcuts.render(request, 'core/index.html', context)