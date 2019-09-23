from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from points.models import leaderboard


class createPointsForm(forms.ModelForm):
    class Meta:
        model = leaderboard
        fields = ('user', 'points')

    def save(self, commit=True):
        points = super(createPointsForm, self).save(commit=False)
        if commit:
            points.save()

        return points
