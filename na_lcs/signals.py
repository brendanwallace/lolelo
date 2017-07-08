from django.db.models import signals
from django import dispatch

from na_lcs import models as na_lcs_models
from na_lcs import util


@dispatch.receiver(signals.post_save, sender=na_lcs_models.Match)
def update_after_match_save(sender, **kwargs):
    pass
    #util.update_ratings_and_predictions()
