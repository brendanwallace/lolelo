import math
import pytz


from django import http
from django import shortcuts

from na_lcs import models as na_lcs_models

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


def nalcs(request):
    # teams:
    teams = na_lcs_models.Team.objects.all().order_by('-rating')
    for team in teams:
        team.rating = '{0:.0f}'.format(team.rating)
        team.make_playoffs = '{:.1f}%'.format(team.make_playoffs * 100)
        team.win_split = '{:.1f}%'.format(team.win_split * 100)
        team.qualify_for_worlds = '{:.1f}%'.format(team.qualify_for_worlds * 100)

    # matches:
    match_predictions_by_week = []
    week = None
    matches = None
    for match in na_lcs_models.Match.objects.filter(team_1_wins=0).filter(team_2_wins=0).order_by('game_number'):
        add_match_predictions(match)
        if week != match.week:
            week = match.week
            matches = []
            match_predictions_by_week.append({'title': 'week {}'.format(week), 'matches': matches})
        matches.append(match)


    context = {
        'teams': teams,
        'match_predictions_by_week': match_predictions_by_week,
        'predictions_selected': 'selected',
        'last_updated': teams[0].last_updated.astimezone(pytz.timezone('US/Pacific')).strftime('%B %d, %Y at %I:%M %p'),
    }
    return shortcuts.render(request, 'na_lcs/nalcs.html', context)

def about(request):
    return shortcuts.render(request, 'na_lcs/about.html', {
        'about_selected': 'selected',
    })