from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework import status
from users.models import User
from branches.models import City
from addresses.models import Address
from django.contrib.gis.geos import Point


class UserTestApi(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        create user in temp database to test the apis
        """
        city = City.objects.create(name='mansoura')
        user = User.objects.create(user_name='omar', password=make_password('123456'))
        User.objects.create_token(user)
        address = Address.objects.create(location=Point(0.0, 0.0), address_info='talkha-mansora', city=city, user=user)

    def test_user_register_api(self):
        """
        test_user_register_api used to test the register api
        it takes the registration data and returns error if the test failed

        """
        url = "/api/user/register/"
        data = {

            'user_name': 'mohamd',
            'password': '123456',

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['id'], 2)
        self.assertEqual(response.data['result']['user_name'], 'mohamd')
        self.assertEqual(response.data['result']['token'],
                         'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwidXNlcl9uYW1lIjoibW9oYW1kIn0.mz8OjI6q2WAd3_05k8Rbeh_tYeuD7y9YwczBmWgZ1Eg')
        self.assertEqual(response.data['message'], "Done")
        self.assertEqual(response.data["status"], True)

    def test_user_login_api(self):
        """
        test_user_login_api used to test the login api
        it takes the login data and returns error if the test failed

        """
        url = "/api/user/login/"
        data = {
            'user_name': 'omar',
            'password': '123456',

        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result']['id'], 1)
        self.assertEqual(response.data['result']['user_name'], 'omar')
        self.assertEqual(response.data['result']['token'],
                         'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwidXNlcl9uYW1lIjoib21hciJ9.Sntk_JIEf6-YT_rg5BBjIO_SJVFPS2K4CXeLidZqesw')
        self.assertEqual(response.data['message'], "Done")
        self.assertEqual(response.data["status"], True)

    def test_user_not_exist_api(self):
        """

        test_user_not_exist_api used to test that only registered users in the database can login
        """
        url = "/api/user/login/"
        data = {

            'user_name': 'ali',
            'password': '123456',

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_response = {

            "non_field_errors": [
                "user not found"
            ]

        }
        self.assertDictEqual(response.json(), test_response)

    def test_user_wrong_password_api(self):
        """
        test_user_wrong_password_api to test the checking of  the password of the user trying to login

        """
        url = "/api/user/login/"
        data = {

            'user_name': 'omar',
            'password': '123455',

        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        test_response = {

            "non_field_errors": [
                "user not found"
            ]

        }
        self.assertDictEqual(response.json(), test_response)
