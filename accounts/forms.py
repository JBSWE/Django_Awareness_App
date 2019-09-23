from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from accounts.models import UserProfile


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username',
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2'
                  )

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email_name = self.cleaned_data['email']

        if commit:
            user.save()
        return user


class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'password',
                  )


class EditUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age',
                  'country',
                  'gender',
                  'education'
                  )

    def save(self, commit=True):
        userprofile = super(EditUserProfileForm, self).save(commit=False)
        if commit:
            userprofile.save()

        return userprofile
