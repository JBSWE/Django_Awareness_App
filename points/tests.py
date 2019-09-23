from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from accounts.models import UserProfile, create_profile
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.urls import reverse
from points import views
from points.models import leaderboard
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.http import HttpResponseRedirect
from django_tables2 import RequestConfig
from points.tables import PointsTable
from django.test.client import RequestFactory


class PointsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.user.first_name = 'jack'

        self.user_profile = UserProfile()
        self.user_profile.user = self.user
        self.user_profile.age = 2
        self.user_profile.country = 'NZ'
        self.user_profile.gender = 'M'
        self.user_profile.education = 'H'

        self.user.save()

        self.login = self.client.login(username='testuser', password='12345')

        self.leaderboard_init = leaderboard()
        self.leaderboard_init.user = self.user
        self.leaderboard_init.points = 0
        self.leaderboard_init.save()

    def test_points_home_view(self):
        url = reverse('points_home')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, self.leaderboard_init.user.leaderboard.points)
        self.assertContains(resp, self.user.first_name)

    def test_points_scores_view(self):
        table = PointsTable(leaderboard.objects.all(), order_by="-points")

        url = reverse('scores')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Leaderboard')
        self.assertContains(resp, self.leaderboard_init.user.username)
        self.assertContains(resp, self.leaderboard_init.points)

    def test_points_getpoints_404_view(self):
        url = reverse('get_points')
        resp = self.client.get(url)

        self.leader = leaderboard.objects.get(user=self.user)
        self.assertEqual(resp.status_code, 404)

    def test_points_getpoints_view(self):
        url = reverse('get_points')
        resp = self.client.get(url+'?score=5')

        self.leader = leaderboard.objects.get(user=self.user)
        self.assertEqual(self.leader.points, 50)
        self.assertEqual(resp.status_code, 200)

    def test_points_pointsdeduct_view(self):
        url = reverse('points_deduct')
        resp = self.client.get(url)

        self.leader = leaderboard.objects.get(user=self.user)

        self.assertEqual(resp.status_code, 302)
        self.assertEqual(self.leader.points, -20)
