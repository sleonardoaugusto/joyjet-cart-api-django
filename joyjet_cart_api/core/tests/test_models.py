from django.test import TestCase

from joyjet_cart_api.core.models import Item, Article, Cart, DeliveryFee


class ItemTest(TestCase):
    def setUp(self):
        self.articles = [Article.objects.create(name="water", price=100),
                         Article.objects.create(name="honey", price=200),
                         Article.objects.create(name="tea", price=1000)]

        self.cart = Cart.objects.create()

        self.items = Item.objects.bulk_create([
            Item(quantity=6, article=self.articles[0], cart=self.cart),
            Item(quantity=2, article=self.articles[1], cart=self.cart),
            Item(quantity=1, article=self.articles[2], cart=self.cart)
        ])

        self.delivery_fees = DeliveryFee.objects.bulk_create([
            DeliveryFee(min_price=0, max_price=999, price=800),
            DeliveryFee(min_price=1000, max_price=1999, price=400),
            DeliveryFee(min_price=2000, max_price=None, price=0)
        ])

    def test_item_amount(self):
        """Return qty * price"""
        expected = 600
        self.assertEqual(expected, self.items[0].item_amount)
        expected = 400
        self.assertEqual(expected, self.items[1].item_amount)
        expected = 1000
        self.assertEqual(expected, self.items[2].item_amount)

    def test_cart_amount(self):
        """Return the sum of all item_amount property"""
        expected = 2000
        self.assertEqual(expected, self.cart.cart_amount)

    def test_get_delivery_fee(self):
        """Return delivery fee price based on total amount"""
        prices = [{'amount': 0, 'expected': 800},
                  {'amount': 999, 'expected': 800},
                  {'amount': 1000, 'expected': 400},
                  {'amount': 1999, 'expected': 400},
                  {'amount': 2000, 'expected': 0},
                  {'amount': 99999, 'expected': 0}]
        for p in prices:
            with self.subTest():
                price = p['expected']
                result = DeliveryFee.get_by_total_amount(p['amount']).price
                self.assertEqual(price, result)
