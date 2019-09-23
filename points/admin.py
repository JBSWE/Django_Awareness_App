from django.contrib import admin
from points.models import leaderboard

# Register your models here.
admin.site.register(leaderboard)
admin.site.site_header = 'CSAP Admin'