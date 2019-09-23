from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete

urlpatterns = [
    url(r'^secure_passwords/$', views.secure_passwords, name='secure_passwords'),
    url(r'^malware/$', views.malware, name='malware')
]
