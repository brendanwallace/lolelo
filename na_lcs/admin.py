from django.contrib import admin
from na_lcs import models as na_lcs_models

# Register your models here.
admin.site.register(na_lcs_models.Team)
admin.site.register(na_lcs_models.Season)
admin.site.register(na_lcs_models.Match)
