import datetime
import math
import pytz


from django import http
from django import shortcuts

from nalcs import models as nalcs_models
from nalcs import util

def index(request):
    return shortcuts.redirect('nalcs')

def na_lcs(request):
    return shortcuts.redirect('nalcs')

def add_match_predictions(match, latest_predictions):
    w1 =  util.expected_outcome(
        latest_predictions[match.team_1.id].rating,
        latest_predictions[match.team_2.id].rating
    )
    w2 = 1 - w1

    p_2_0 = w1 * w1
    p_0_2 = w2 * w2

    p_2_1 = w1*w2*w1 + w2*w1*w1
    p_1_2 = w2*w1*w2 + w1*w2*w2

    match.team_1_win_p = '{0:.0f}%'.format(100 * (p_2_0 + p_2_1))
    match.team_2_win_p = '{0:.0f}%'.format(100 * (p_0_2 + p_1_2))

    match.p_2_0 = '{0:.0f}%'.format(100 * p_2_0)
    match.p_2_1 = '{0:.0f}%'.format(100 * p_2_1)
    match.p_1_2 = '{0:.0f}%'.format(100 * p_1_2)
    match.p_0_2 = '{0:.0f}%'.format(100 * p_0_2)


def nalcs(request):
    # TODO - filter on league
    nalcs_teams = nalcs_models.Team.objects.all()

    # For every day that there are predictions, there should be one
    # DailyPrediction per team, so if we order by date and limit results to the
    # number of teams we're guaranteed to get one for each team.
    latest_predictions = {
        p.team.id: p
        for p in nalcs_models.DailyPrediction.objects
            .filter(team__in=nalcs_teams).order_by('-date')[:len(nalcs_teams)]
    }

    one_week_ago = datetime.datetime.today().date() - datetime.timedelta(days=3)
    comparison_predictions = {
        p.team_id: p
        for p in 
        nalcs_models.DailyPrediction.objects
            .filter(team__in=nalcs_teams)
            .filter(date__lte=one_week_ago)
            .order_by('-date')[:len(nalcs_teams)]
    }


    for team_id, prediction in latest_predictions.items():
        prediction.name = prediction.team.name

        prediction.rating_display = '{0:.0f}'.format(prediction.rating)
        prediction.make_playoffs_display = '{:.1f}%'.format(prediction.make_playoffs * 100)
        prediction.win_split_display = '{:.1f}%'.format(prediction.win_split * 100)
        prediction.qualify_for_worlds_display = '{:.1f}%'.format(prediction.qualify_for_worlds * 100)

        rating_delta = prediction.rating - comparison_predictions[team_id].rating
        if abs(rating_delta) > 5:
            prediction.rating_delta = '{0:.0f}'.format(rating_delta)
            prediction.rating_delta_sign = 'down' if rating_delta < 0 else 'up'

        make_playoffs_delta = prediction.make_playoffs - comparison_predictions[team_id].make_playoffs
        if abs(make_playoffs_delta) > 0.05:
            prediction.make_playoffs_delta = '{:.1f}%'.format((make_playoffs_delta)  * 100)
            prediction.make_playoffs_delta_sign = 'down' if prediction.make_playoffs_delta[0] == '-' else 'up'

        win_split_delta = prediction.win_split - comparison_predictions[team_id].win_split
        if abs(win_split_delta) > 0.02:
            prediction.win_split_delta = '{:.1f}%'.format((prediction.win_split - comparison_predictions[team_id].win_split)  * 100)
            prediction.win_split_delta_sign = 'down' if prediction.win_split_delta[0] == '-' else 'up'

        qualify_for_worlds_delta = prediction.qualify_for_worlds - comparison_predictions[team_id].qualify_for_worlds
        if abs(qualify_for_worlds_delta) > 0.02:
            prediction.qualify_for_worlds_delta = '{:.1f}%'.format((qualify_for_worlds_delta)  * 100)
            prediction.qualify_for_worlds_delta_sign = 'down' if prediction.qualify_for_worlds_delta[0] == '-' else 'up'

    # matches:
    match_predictions_by_week = []
    week = None
    matches = None
    for match in nalcs_models.Match.objects.filter(team_1_wins=0).filter(team_2_wins=0).order_by('game_number'):
        add_match_predictions(match, latest_predictions)
        if week != match.week:
            week = match.week
            matches = []
            match_predictions_by_week.append({'title': 'week {}'.format(week), 'matches': matches})
        matches.append(match)


    context = {
        'teams': sorted([p for _, p in latest_predictions.items()], key=lambda t: t.rating, reverse=True),
        'match_predictions_by_week': match_predictions_by_week,
        'predictions_selected': 'selected',
        'last_updated': latest_predictions[nalcs_teams[0].id].last_updated.astimezone(pytz.timezone('US/Pacific')).strftime('%B %d, %Y at %I:%M %p'),
    }
    return shortcuts.render(request, 'nalcs/nalcs.html', context)

def about(request):
    return shortcuts.render(request, 'nalcs/about.html', {
        'about_selected': 'selected',
    })