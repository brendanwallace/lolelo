from django.contrib import admin
from core import models as core_models

# Register your models here.
admin.site.register(core_models.Team)
admin.site.register(core_models.Season)
admin.site.register(core_models.Match)
