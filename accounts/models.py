from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_countries.fields import CountryField
from datetime import datetime
from django.core.mail import send_mail


# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    age = models.IntegerField(default=0)
    country = CountryField(blank_label='(select country)')
    GENDER_CHOICES = (
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=False, null=False, default='')
    EDUCATION_CHOICES = (
        ('', 'Select Education'),
        ('H', 'High School'),
        ('U', 'Undergraduate'),
        ('P', 'Postgraduate'),
    )
    education = models.CharField(max_length=1, choices=EDUCATION_CHOICES, blank=False, null=False, default='')
def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)


class MailText(models.Model):
    subject = models.CharField(max_length=30)
    message = models.TextField(max_length=1000)
    users = User.objects.all()
    send_it = models.BooleanField(default=False)
    def save(self):
        if self.send_it:
            # create your list of users
            user_list = []
            for u in self.users:
                user_list.append(u.email)
            # send the message.
            send_mail(str(self.subject),
                      str(self.message),
                      'csapnoreply@gmail.com',
                      user_list,
                      fail_silently=False)
    class Meta:
        verbose_name = "Send Email to All Users"
        verbose_name_plural = "Send Email to All Users"
