from django.contrib import admin
from accounts.models import UserProfile, MailText

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(MailText)
admin.site.site_header = 'CSAP Admin'
