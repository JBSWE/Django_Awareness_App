from django.shortcuts import render, HttpResponse, redirect
from accounts.forms import RegistrationForm, EditProfileForm, EditUserProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from points.forms import createPointsForm
from points.models import leaderboard
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field


# Create your views here.
@login_required
def home(request):
    leaderboard_init = leaderboard.objects.get(user=request.user)

    args = {'user': request.user,
            'points': leaderboard_init.points
            }
    return render(request, 'accounts/home.html', args)


def register(request):
    if request.method == 'POST':

        form = RegistrationForm(request.POST)
        if form.is_valid():
            formuser = form['username'].value()
            form.save()

            user_get = User.objects.get(username=formuser)

            leaderboard_init = leaderboard()
            leaderboard_init.user = user_get
            leaderboard_init.points = 0
            leaderboard_init.save()

            return redirect('/account/login/')
    else:
        form = RegistrationForm()

        args = {'form': form
                }
        return render(request, 'accounts/reg_form.html', args)


@login_required
def profile(request):
    args = {
        'user': request.user,
        'details': request.user.userprofile
    }

    return render(request, 'accounts/profile.html', args)

@login_required
def edituserprofile(request):
    if request.method == 'POST':
        form = EditUserProfileForm(request.POST, instance=request.user.userprofile)
        form.user = request.user
        if form.is_valid():
            form.save()

            return redirect('/account/profile')
    else:
        form = EditUserProfileForm(instance=request.user.userprofile)
        args = {'form': form}

        return render(request, 'accounts/edituserprofile.html', args)


@login_required
def editprofile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()

            return redirect('/account/profile')
    else:
        form = EditProfileForm(instance=request.user)
        args = {'form': form}

        return render(request, 'accounts/editprofile.html', args)


@login_required
def edit_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('/account/profile')
        else:
            return redirect('accounts/editpassword')

    else:
        form = PasswordChangeForm(user=request.user)
        args = {'form': form}

        return render(request, 'accounts/editpassword.html', args)
