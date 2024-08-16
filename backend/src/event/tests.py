from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Event
from datetime import date

# Create your tests here.
class EventAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = '/event/'
        self.PostResponse = None
        self.GetResponse = None
        self.payload = {
            'hotel_id': 1,
            'room_id': '00aa00a0-0aa0-0a0a-aa00-000000a0000a',
            'rpg_status': 1,
            'night_of_stay': '2024-08-17'
        }
        self.test_create_event()
        self.test_retrieve_event()


    def test_create_event(self):
        self.PostResponse = self.client.post(self.url, self.payload, format='json')
        self.assertIsNotNone(self.PostResponse)

    def test_correct_status_code_on_create_event(self):
        self.assertEqual(self.PostResponse.status_code, status.HTTP_201_CREATED)

    def test_data_inserted_to_db(self):
        self.assertEqual(Event.objects.count(), 1)

    def test_data_creation_validity(self):
        event = Event.objects.get()
        self.assertEqual(event.hotel_id, self.payload.get('hotel_id'))
        self.assertEqual(event.room_id, self.payload.get('room_id'))
        self.assertEqual(event.rpg_status, self.payload.get('rpg_status'))
        self.assertEqual(event.night_of_stay, date(2024, 8, 17))
        self.assertIsNotNone(event.timestamp)

    def test_retrieve_event(self):
        self.GetResponse = self.client.get(f"{self.url}1/")
        self.assertIsNotNone(self.GetResponse)
        
    def test_correct_status_code_on_get_event(self):
        self.assertEqual(self.GetResponse.status_code, 200)

    def test_get_data_validity(self):
        response_data = self.GetResponse.json()
        self.assertEqual(response_data['hotel_id'], self.payload.get('hotel_id'))
        self.assertEqual(response_data['room_id'], self.payload.get('room_id'))
        self.assertEqual(response_data['rpg_status'], self.payload.get('rpg_status'))
        self.assertEqual(response_data['night_of_stay'], self.payload.get('night_of_stay'))
        self.assertIn('timestamp', response_data)