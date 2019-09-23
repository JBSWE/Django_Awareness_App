from django.shortcuts import render, redirect
from points.models import leaderboard
from django_tables2 import RequestConfig
from points.tables import PointsTable
from django.http import Http404
# Create your views here.
def home(request):
    leaderboard_init = leaderboard.objects.get(user=request.user)

    args = {'user': request.user,
            'points': leaderboard_init.points
            }
    return render(request, 'accounts/home.html', args)

def scores(request):
    table = PointsTable(leaderboard.objects.all(), order_by="-points")
    RequestConfig(request).configure(table)
    return render(request, 'points/leaderboard.html', {'table': table})

def points_deduct(request):

    leaderboard_deduct = leaderboard.objects.get(user=request.user)
    leaderboard_deduct.points = leaderboard_deduct.points - 20
    leaderboard_deduct.save()

    return redirect("https://google.com/")

def get_points(request):
    score = request.GET.get('score')

    try:
        leaderboard_deduct = leaderboard.objects.get(user=request.user)
        leaderboard_deduct.points = leaderboard_deduct.points + (int(score) * 10)
        leaderboard_deduct.save()

        args = {'user': request.user,
                'points': (int(score) * 10),
                'score': score
                }
        return render(request, 'points/results.html', args)
    except TypeError:
        raise Http404("Cannot get your points")
