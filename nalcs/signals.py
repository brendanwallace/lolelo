from django.db.models import signals
from django import dispatch

from nalcs import models as nalcs_models
from nalcs import util


@dispatch.receiver(signals.post_save, sender=nalcs_models.Match)
def update_after_match_save(sender, **kwargs):
    pass#util.update_ratings_and_predictions()
