from django.test import TestCase, Client
from django.urls import reverse
from .models import GeolocatorStats

class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view_with_valid_input_name(self):
        response = self.client.post(reverse('homepage'), {'query': 'New York'})
        self.assertEqual(response.status_code, 200)

        # Check if the GeolocatorStats object was created in the database
        self.assertEqual(GeolocatorStats.objects.count(), 1)

        # Check if the response contains the expected data
        self.assertContains(response, 'New York')
        self.assertContains(response, 'Latitude')
        self.assertContains(response, 'Longitude')
        
    def test_index_view_with_valid_input_coordinates(self):
        response = self.client.post(reverse('homepage'), {'query': '43.8519774, 18.3866868'})
        self.assertEqual(response.status_code, 200)

        # Check if the GeolocatorStats object was created in the database
        self.assertEqual(GeolocatorStats.objects.count(), 1)

        # Check if the response contains the expected data
        self.assertContains(response, 'EP BiH')
        self.assertContains(response, 'Latitude')
        self.assertContains(response, 'Longitude')

    def test_index_view_with_invalid_input(self):
        response = self.client.post(reverse('homepage'), {'query': 'dfbvkjsdbnikcn'})
        self.assertEqual(response.status_code, 200)

        # Check if the error message is present in the response
        self.assertContains(response, 'Could not find the location')

        # Check that no GeolocatorStats object was created in the database
        self.assertEqual(GeolocatorStats.objects.count(), 0)
