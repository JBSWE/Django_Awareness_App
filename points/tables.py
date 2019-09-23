import django_tables2 as tables
from points.models import leaderboard


class PointsTable(tables.Table):
    class Meta:
        model = leaderboard
        template_name = 'django_tables2/bootstrap.html'
        fields = ('user', 'points')
