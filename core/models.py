from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name
    rating = models.FloatField(default=0)
    match_wins = models.IntegerField(default=0)
    match_losses = models.IntegerField(default=0)
    game_wins = models.IntegerField(default=0)
    game_losses = models.IntegerField(default=0)


class Season(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    def __str__(self):
        return self.name

# Scheduled match -- doesn't contain results
class Match(models.Model):
    team_1 = models.ForeignKey('Team', related_name='team_1_match')
    team_2 = models.ForeignKey('Team', related_name='team_2_match')
    week = models.IntegerField()
    # TODO - this should really be date field not integer field:
    game_number = models.IntegerField()
    best_of = models.IntegerField()
    season = models.ForeignKey('Season')
    # results:
    team_1_wins = models.IntegerField(default=0)
    team_2_wins = models.IntegerField(default=0)
    def __str__(self):
        string = '{}, week {}: {} vs {}'.format(
            str(self.season), str(self.week), str(self.team_1), str(self.team_2)
        )
        if self.team_1_wins + self.team_2_wins > 0:
            string += ': {} - {}'.format(str(self.team_1_wins), str(self.team_2_wins))
        return string
