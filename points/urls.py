from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.home, name='points_home'),
    url(r'^leaderboard/$', views.scores, name='scores'),
    url(r'^instantaccess/$', views.points_deduct, name='points_deduct'),
    url(r'^getpoints/$', views.get_points, name='get_points'),

]