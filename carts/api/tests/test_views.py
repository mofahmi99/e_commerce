from django.contrib.auth.hashers import make_password

from django.test import TestCase
from rest_framework import status, request

from carts.models import Cart
from products.models import Item, Category
from users.models import User
from branches.models import City
from addresses.models import Address
from django.contrib.gis.geos import Point


class CartTestApi(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        create cart and cart items in temp database to test the apis
        """
        user = User.objects.create(user_name='omar', password=make_password('123456'))
        User.objects.create_token(user)
        city = City.objects.create(name='mansoura')
        user_address = Address.objects.create(location=Point(0.0, 0.0), address_info='talkha-mansora', city=city,
                                              user=user)
        cart = Cart.objects.create(address=user_address)
        category = Category.objects.create(title='food')
        item = Item.objects.create(price=210, is_available=True, title='gum', description='mango flavored gum')
        item.categories.set([category])
        item.save()


    def test_add_product(self):
        """
        test add_product to cart api

        """
        url = "/api/cart/add_product/?address_id=1"
        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        data = {

            'quantity': '5',
            'item_id': '1',

        }
        response = self.client.post(url, data, format='json', **headers)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_carts(self):
        """
        test cart api
        """
        url = "/api/cart/details/"
        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

