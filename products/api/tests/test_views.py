import json

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
        item = Item.objects.create(price=210, is_available=True, title='gum', description='mango flavored gum')
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
        # print(response.data)
        # test_response = {
        #     "result": {
        #         "id": response.data['result'][0]['id'],
        #         "created_at": response.data['result'][0]['created_at'],
        #         "updated_at": response.data['result'][0]['updated_at'],
        #         "price": response.data['result'][0]['price'],
        #         "is_available": response.data['result'][0]['is_available'],
        #         "branch": {
        #             "branch_id": response.data['result'][0]['branch']['branch_id'],
        #             "branch__name": response.data['result'][0]['branch']['branch__name'],
        #         },
        #
        #         "categories": [
        #             response.data['result'][0]['categories'][0]
        #         ],
        #         "title": response.data['result'][0]['title'],
        #         "image": response.data['result'][0]['image'],
        #         "description": response.data['result'][0]['description']
        #     },
        #     "message": response.data['message'],
        #     "status": response.data['status'],
        # }
        # print(test_response)
        # self.assertDictEqual(response.json(), test_response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_product_list_api_wrong_address(self):
        url = "/api/products/product/?address_id=2&category_id=1"

        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
