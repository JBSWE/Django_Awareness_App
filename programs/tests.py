from django.test import TestCase
from django.urls import reverse


# Create your tests here.
class ProgramsTest(TestCase):
    def test_secure_passwords_view(self):
        url = reverse('secure_passwords')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)

    def test_malware_view(self):
        url = reverse('malware')
        resp = self.client.get(url)

        self.assertEqual(resp.status_code, 200)
