from datetime import timedelta

from django.core.management.base import BaseCommand

from nalcs import models as nalcs_models

class Command(BaseCommand):
    def handle(self, *args, **options):
        for season in nalcs_models.Season.objects.all():
            date = season.date
            matches = iter(nalcs_models.Match.objects.filter(season=season).order_by('game_number'))
            # 9 weeks
            for i in range(5):
                # Friday
                for i in range(2):
                    match = next(matches)
                    match.date = date
                    match.save()
                # Saturday
                date += timedelta(days=1)
                for i in range(4):
                    match = next(matches)
                    match.date = date
                    match.save()
                # Sunday
                date += timedelta(days=1)
                for i in range(4):
                    match = next(matches)
                    match.date = date
                    match.save()
                date += timedelta(days=5)
            # after week 5, break for one week (not sure how long this has been
            # the rule for.
            date += timedelta(days=7)
            for i in range(4):
                # Friday
                for i in range(2):
                    match = next(matches)
                    match.date = date
                    match.save()
                # Saturday
                date += timedelta(days=1)
                for i in range(4):
                    match = next(matches)
                    match.date = date
                    match.save()
                # Sunday
                date += timedelta(days=1)
                for i in range(4):
                    match = next(matches)
                    match.date = date
                    match.save()
                date += timedelta(days=5)



