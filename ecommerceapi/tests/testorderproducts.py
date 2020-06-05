from django.test import TestCase
from django.urls import reverse
from ecommerceapi.models import Product, Customer, Order, OrderProduct, ProductType, PaymentType
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from unittest import skip

"""
- Maybe this will work
"""

class TestOrderProducts(TestCase):
    # Set up all data that will be needed to excute all the tests in the test file.
    def setUp(self):
        pass
        self.username = "KittyBaby"
        self.password = "KittyBabyNumber1"
        self.user = User.objects.create_user(
            username=self.username, password=self.password)
        self.token = Token.objects.create(user=self.user)
        self.customer = Customer.objects.create(
            user_id=1, address="808 Kitty Baby Blvd", phone_number="615-Kitty-Bae")

    def testPost(self):
        pass
    
    def testList(self):
        thisOrder = Order.objects.create(
            created_at="2020-06-03 00:00:00Z",
            customer_id=1,
            payment_type_id=1)
        furby = Product.objects.create(
            title="Furby",
            customer_id=1,
            price=3.00,
            description="Demon baby from hell",
            quantity=4, 
            location="Nashville",
            image_path="https://upload.wikimedia.org/wikipedia/en/7/70/Furby_picture.jpg",
            created_at="2020-06-03 00:00:00Z",
            product_type_id = 1)
        toys = ProductType.objects.create(name="Toys")
        pt = PaymentType.objects.create(
            merchant_name="Stupid Company", 
            account_number="1234123412341234", 
            expiration_date="2024-01-01", 
            customer_id=1, 
            created_at="2020-05-27 15:08:30.518598Z")
        order_product = OrderProduct.objects.create(order_id = 1, product_id = 1)

        response = self.client.get(
            reverse('orderproducts-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 1)

    def testDelete(self):
        new_orderproduct = OrderProduct.objects.create(
            order_id=1,
            product_id=1
        )

        response = self.client.get(
            reverse('orderproducts-list'), HTTP_AUTHORIZATION='Token ' + str(self.token))

        self.assertEqual(len(response.data), 1)

    def testOrderIdQuery(self):
        pass

if __name__ == '__main__':
    unittest.main()
