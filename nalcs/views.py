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

def add_predictions_to_match(match: nalcs_models.Match, latest_predictions) -> None:
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

class Week():
    def __init__(self, week):
        self.week = week
        self.dates = []

class Date():
    def __init__(self, date):
        self.date = date
        self.matches = []


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

    # active_week is the latest week in which a game hasn't been played
    active_week = None
    # matches grouped by week, then by date, sorted by game number
    all_matches = []
    curr_week = Week(None)
    curr_date = Date(None)
    for match in nalcs_models.Match.objects.filter(season__name='Summer 2017').order_by('game_number'):
        if curr_week.week != match.week:
            curr_week = Week(match.week)
            all_matches.append(curr_week)
        if curr_date.date != match.date:
            curr_date = Date(match.date) # 'title': match.date.strftime('%B %d')}
            curr_week.dates.append(curr_date)
        if not match.finished:
            add_predictions_to_match(match, latest_predictions)
            if not active_week:
                active_week = match.week
        curr_date.matches.append(match)

    context = {
        'teams': sorted([p for _, p in latest_predictions.items()], key=lambda t: t.rating, reverse=True),
        'all_matches': all_matches,
        'predictions_selected': 'selected',
        'last_updated': (
            latest_predictions[nalcs_teams[0].id].last_updated.astimezone(
                pytz.timezone('US/Pacific')).strftime('%B %d, %Y at %I:%M %p')
        ),
        # TODO - get this from the current date.
        'week_to_toggle': active_week,
    }
    return shortcuts.render(request, 'nalcs/nalcs.html', context)

def about(request):
    return shortcuts.render(request, 'nalcs/about.html', {
        'about_selected': 'selected',
    })