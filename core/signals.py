from django.db.models import signals
from django import dispatch

from core import models as core_models
from core import util


@dispatch.receiver(signals.post_save, sender=core_models.Match)
def update_after_match_save(sender, **kwargs):
    util.update_ratings_and_predictions()