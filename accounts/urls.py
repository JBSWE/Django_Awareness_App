from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}),
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/edit$', views.editprofile, name='editprofile'),
    url(r'^profile/editpassword$', views.edit_password, name='editpassword'),
    url(r'^resetpassword$', password_reset, name='resetpassword'),
    url(r'^resetpassword/done$', password_reset_done, name='password_reset_done'),
    url(r'^resetpassword/confirm(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^resetpassword/complete$', password_reset_complete, name='password_reset_complete'),
    url(r'^profile/edituserprofile$', views.edituserprofile, name='edituserprofile'),
]
