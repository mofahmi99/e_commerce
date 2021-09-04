from django.contrib.auth.hashers import make_password

from django.test import TestCase
from rest_framework import status, request

from carts.models import Cart, CartItem
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
                                              user=user, title='home')
        cart = Cart.objects.create(address=user_address)
        category = Category.objects.create(title='food')
        item = Item.objects.create(price=210, is_available=True, title='gum', description='mango flavored gum')
        item.categories.set([category])
        item.save()
        cart_item = CartItem.objects.create(cart_id=cart.id, item_id=item.id, quantity=5, price=10)

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
        print(response.data['result'])
        self.assertEqual(response.data['result']['id'], 1)
        self.assertEqual(response.data['result']['items'][0]['id'], 1)
        self.assertEqual(response.data['result']['items'][0]['item_total'], "50.00 SAR", )
        self.assertEqual(response.data['result']['items'][0]['price'], "10.00 SAR", )
        self.assertEqual(response.data['result']['items'][0]['quantity'], 5)
        self.assertEqual(response.data['result']['items'][0]['cart'], 1)
        self.assertEqual(response.data['result']['items'][0]['item'], 1)
        self.assertEqual(response.data['result']['items'][0]['name'], 'gum')
        self.assertEqual(response.data['result']['items'][0]['description'], 'mango flavored gum')
        self.assertEqual(response.data['result']['cart_total'], "50.00 SAR")
        self.assertEqual(response.data['result']['grand_total'], "70.00 SAR")
        self.assertEqual(response.data['result']['shipping_fee'], "20 SAR")
        self.assertEqual(response.data['result']['address']['title'], "home")
        self.assertEqual(response.data['result']['address']['city'], "mansoura")
        self.assertEqual(response.data['result']['address']['details'], "talkha-mansora")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
            'item_id': 1,
            'quantity': 20

        }
        response = self.client.post(url, data, format='json', **headers)
        print(response.data['result'])
        self.assertEqual(response.data['result']['id'], 1)
        self.assertEqual(response.data['result']['item_total'], "200.00 SAR", )
        self.assertEqual(response.data['result']['price'], "10.00 SAR", )
        self.assertEqual(response.data['result']['quantity'], 20, )
        self.assertEqual(response.data['result']['cart'], 1)
        self.assertEqual(response.data['result']['item'], 1)
        self.assertEqual(response.data['result']['name'], 'gum')
        self.assertEqual(response.data['result']['description'], 'mango flavored gum')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

