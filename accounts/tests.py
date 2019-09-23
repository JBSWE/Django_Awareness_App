from django.test import TestCase, Client
from accounts.models import UserProfile, create_profile
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from django.urls import reverse
from accounts import views
from points.models import leaderboard
from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_reset_confirm, \
    password_reset_complete
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver



# Create your tests here.


class AccountsTest(TestCase):
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

    def test_account_login_view(self):
        url = reverse(login)
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'You are already logged in')

    def test_account_register_view(self):
        url = reverse('register')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Register')

    def test_account_register_valid(self):
        args = {
            'username': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'email': 'test@test.com',
            'password1': 'hello123?',
            'password2': 'hello123?'
        }
        response = self.client.post(
            reverse('register'), args)

        self.assertRedirects(response, '/account/login/')
        self.assertEqual(response.status_code, 302)

    def test_account_home_view(self):
        self.leaderboard_init = leaderboard()
        self.leaderboard_init.user = self.user
        self.leaderboard_init.points = 0
        self.leaderboard_init.save()

        url = reverse('home')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'You currently have 0 points!')
        self.assertContains(resp, 'jack')

    def test_account_profile_view(self):
        url = reverse('profile')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'jack')

    def test_account_editpassword_view(self):
        url = reverse('editpassword')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Change Password')

    def test_account_editpassword_view_post_valid(self):
        args = {
            'old_password': '12345',
            'new_password1': 'hello123',
            'new_password2': 'hello123'
        }
        response = self.client.post(
            reverse('editpassword'), args)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/profile')

    def test_account_editpassword_view_post_invalid(self):
        args = {
            'old_password': '12345a',
            'new_password1': 'hello123?',
            'new_password2': 'hello123?'
        }
        response = self.client.post(
            reverse('editpassword'), args)

        # c.post('/login/', {'name': 'fred', 'passwd': 'secret'})
        # url = reverse('editpassword')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, 'accounts/editpassword')
        # self.assertTrue(User.objects.filter(
        #     first_name='Test').exists())

    def test_account_edituserprofile_valid(self):
        args = {
            'age': 30,
            'country': 'NZ',
            'gender': 'M',
            'education': 'H',
        }
        response = self.client.post(
            reverse('edituserprofile'), args)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/profile')

    def test_account_edituserprofile_invalid(self):
        url = reverse('edituserprofile')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Edit Profile')

    def test_account_editprofile_valid(self):
        args = {
            'first_name': 'jack',
            'last_name': 'kk',
            'email': 'kk@kk.com',
            'password': self.user.password
        }
        response = self.client.post(
            reverse('editprofile'), args)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/profile')

    def test_account_editprofile_invalid(self):
        url = reverse('editprofile')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Edit Profile')

    def tearDown(self):
        self.user.delete()
        # self.user_profile.delete()

# class MySeleniumTests(StaticLiveServerTestCase):
#     @classmethod
#     def setUpClass(cls):
#         User.objects.create_user(username='user', password='pass', email='test@test.com')
#         super(MySeleniumTests, cls).setUpClass()
#         cls.selenium = WebDriver()
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super(MySeleniumTests, cls).tearDownClass()
#
#     def test_register(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/account/register/'))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('testing')
#         first_name_input = self.selenium.find_element_by_name("first_name")
#         first_name_input.send_keys('jack')
#         last_name_input = self.selenium.find_element_by_name("last_name")
#         last_name_input.send_keys('burke')
#         email_input = self.selenium.find_element_by_name("email")
#         email_input.send_keys('j.burke1@newcastle.ac.uk')
#         password1_input = self.selenium.find_element_by_name("password1")
#         password1_input.send_keys('hello123?')
#         password2_input = self.selenium.find_element_by_name("password2")
#         password2_input.send_keys('hello123?')
#
#         submit = self.selenium.find_element_by_xpath("//button[text()='Submit']")
#         submit.send_keys(Keys.RETURN)
#
#     def test_login(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/account/login/'))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('user')
#         password_input = self.selenium.find_element_by_name("password")
#         password_input.send_keys('pass')
#         self.selenium.find_element_by_xpath("//button[text()='Login']").click()
#
#     def test_home(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/account/'))

class SeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()


    # def test_user_logout(self):
    #     self.browser.get(self.live_server_url + '/account/logout')
    #     self.browser.find_element_by_link_text('Logout').click()
    #     #self.assertEqual('Welcome jack', str(self.browser.find_element_by_id("name-text").text))






    def test_account_features(self):
        #self.browser.get('http://localhost:8000/account/register')
        #self.browser.get(self.live_server_url + '/account/register')

        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('pop123pop1qq')
        first_name_input = self.browser.find_element_by_name("first_name")
        first_name_input.send_keys('jack')
        last_name_input = self.browser.find_element_by_name("last_name")
        last_name_input.send_keys('burke')
        email_input = self.browser.find_element_by_name("email")
        email_input.send_keys('popop@popo.com')
        password1_input = self.browser.find_element_by_name("password1")
        password1_input.send_keys('hello123?')
        password2_input = self.browser.find_element_by_name("password2")
        password2_input.send_keys('hello123?')

        self.browser.find_element_by_xpath("//button[text()='Submit']").click()

        username_input = self.browser.find_element_by_name("username")
        username_input.send_keys('pop123pop1')
        password_input = self.browser.find_element_by_name("password")
        password_input.send_keys('hello123?')
        self.browser.find_element_by_xpath("//button[text()='Login']").click()
        self.assertEqual('Welcome jack', str(self.browser.find_element_by_id("name-text").text))

    # def test_account_profile_edit:
    #     self.browser.find_element_by_link_text('Profile').click()
    #     self.browser.find_element_by_id('edit_profile').click()
    #
    #     fist_name_input = self.browser.find_element_by_name("first_name")
    #     first_name_input.send_keys('john')
    #     last_name_input = self.browser.find_element_by_name("last_name")
    #     last_name_input.send_keys('doe')
    #     email_input = self.browser.find_element_by_name("email")
    #     email_input.send_keys('john@doe.com')
    #
    #     # self.assertEqual('Welcome jack', str(self.browser.find_element_by_id("name-text").text))






