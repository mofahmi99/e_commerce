from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework import status
from users.models import User
from branches.models import City
from addresses.models import Address
from django.contrib.gis.geos import Point


class AddressTestApi(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        create user in temp database to test the apis
        """
        city = City.objects.create(name='mansoura')
        user = User.objects.create(user_name='omar', password=make_password('123456'))
        User.objects.create_token(user)

    def test_add_address_api(self):
        """
       test_create_address_api used to test the creation of a user address

        """
        url = "/api/address/add_address/"
        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        data = {

            "address_info": "talkha-kfourelarab",
            "city": 1,
            "user": 1,
            "title": "work",
            "location": "SRID=4326;POINT (50.3658 -95.677068)"

        }

        response = self.client.post(url, data, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result']['id'], 1)
        self.assertEqual(response.data['result']['title'], 'work')
        self.assertEqual(response.data['result']['address_info'], 'talkha-kfourelarab')
        self.assertEqual(response.data['result']['location'], "SRID=4326;POINT (50.3658 -95.67706800000001)")
        self.assertEqual(response.data['message'], "Done")
        self.assertEqual(response.data["status"], True)

