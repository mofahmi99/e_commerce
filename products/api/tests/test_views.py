import json
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from users.models import User
from addresses.models import Address
from products.models import Item, Category
from branches.models import BranchItem, Branch, City
from django.contrib.gis.geos import Point


class ProductList(TestCase):
    @classmethod
    def setUpTestData(cls):
        """
        create item and branchitem in temp database to test the api
        """
        city = City.objects.create(name='mansoura')
        user = User.objects.create(user_name='omar', password=make_password('123456'))
        User.objects.create_token(user)
        address = Address.objects.create(location=Point(0.0, 0.0), address_info='talkha-mansora', city=city, user=user)
        category = Category.objects.create(title='food')
        item = Item.objects.create(price=210, is_available=True, title='gum', description='mango flavored gum',
                                   created_at='04.09.2021 01:47', updated_at='04.09.2021 01:47')
        item.categories.set([category])
        item.save()
        branch = Branch.objects.create(name='talkha', city=city)
        BranchItem.objects.create(branch=branch, item=item, is_available=True, price=190)

    def test_product_list_api(self):
        url = "/api/products/product/?address_id=1&category_id=1"

        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.get(url, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['id'], 1)
        self.assertEqual(response.data['result'][0]['created_at'], '04.09.2021 02:04')
        self.assertEqual(response.data['result'][0]['updated_at'], '04.09.2021 02:04')
        self.assertEqual(response.data['result'][0]['price'], "190.00 SAR")
        self.assertEqual(response.data["result"][0]["is_available"], True)
        self.assertEqual(response.data['result'][0]['branch'][0], 'talkha')
        self.assertEqual(response.data['result'][0]['title'], 'gum')
        self.assertEqual(response.data['result'][0]['image'], None)
        self.assertEqual(response.data['result'][0]['description'], "mango flavored gum")
        self.assertEqual(response.data["status"], True)
        self.assertEqual(response.data['message'], "Retrieved Successfully")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_api_wrong_address(self):
        url = "/api/products/product/?address_id=2&category_id=1"

        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.data["status"], False)
        self.assertEqual(response.data['message'], "Wrong Address")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_list_api_wrong_category(self):
        url = "/api/products/product/?address_id=1&category_id=10"

        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.data["status"], False)
        self.assertEqual(response.data['message'], "no items found")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
