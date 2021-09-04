from django.contrib.auth.hashers import make_password
from django.test import TestCase
from rest_framework import status

from carts.models import Cart
from orders.models import Order, OrderProduct
from products.models import Category, Item
from users.models import User
from branches.models import City
from addresses.models import Address
from django.contrib.gis.geos import Point


class OrderTestApi(TestCase):

    @classmethod
    def setUpTestData(cls):
        """
        create order to test the apis
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
        order = Order.objects.create(user=user, address=user_address, order_total=150, shipping_fee=0, grand_total=150)
        order_product = OrderProduct.objects.create(order=order, item=item, quantity=5, price=item.price)

    def test_create_order(self):
        """
         test create_order api
        """
        url = "/api/order/create_order/?address_id=1"
        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.post(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['result']['id'], 2)
        self.assertEqual(response.data['result']['order_total'], "0 SAR", )
        self.assertEqual(response.data['result']['grand_total'], "20 SAR", )
        self.assertEqual(response.data['result']['shipping_fee'], "20 SAR", )
        self.assertEqual(response.data['result']['delivery_date'], "2021-09-04")
        self.assertEqual(response.data['result']['user'], 1)
        self.assertEqual(response.data['result']['address'][0]['title'], 'home')
        self.assertEqual(response.data['result']['address'][0]['city'], 1)
        self.assertEqual(response.data['result']['address'][0]['address_info'], 'talkha-mansora')

    def test_list_order(self):
        """
        test order list api
        """
        url = "/api/order/details/"
        user_token = User.objects.first().token
        headers = {
            'HTTP_AUTHORIZATION': 'Bearer ' + user_token
        }
        response = self.client.get(url, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'][0]['id'], 1)
        self.assertEqual(response.data['result'][0]['order_total'], "150.00 SAR", )
        self.assertEqual(response.data['result'][0]['grand_total'], "150.00 SAR", )
        self.assertEqual(response.data['result'][0]['shipping_fee'], "0.00 SAR", )
        self.assertEqual(response.data['result'][0]['delivery_date'], "2021-09-04")
        self.assertEqual(response.data['result'][0]['user'], 1)
        self.assertEqual(response.data['result'][0]['address'][0]['title'], 'home')
        self.assertEqual(response.data['result'][0]['address'][0]['city'], 1)
        self.assertEqual(response.data['result'][0]['address'][0]['address_info'], 'talkha-mansora')
