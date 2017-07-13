from django.contrib import admin
from nalcs import models as nalcs_models

# Register your models here.
admin.site.register(nalcs_models.Team)
admin.site.register(nalcs_models.Season)
admin.site.register(nalcs_models.Match)
