from django.test import TestCase

from joyjet_cart_api.core.models import (
    Item,
    Article,
    Cart,
    DeliveryFee,
    Discount
)


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

        self.discounts = Discount.objects.create(disc_type='amount', value=25, article_id=2)

    def test_item_amount(self):
        """Return qty * price"""
        amount = 600
        self.assertEqual(amount, self.items[0].item_amount)
        amount = 350
        self.assertEqual(amount, self.items[1].item_amount)
        amount = 1000
        self.assertEqual(amount, self.items[2].item_amount)

    def test_cart_price(self):
        """Return the sum of all items amount"""
        amount = 2350
        self.assertEqual(amount, self.cart.price)

    def test_get_delivery_fee(self):
        """Return delivery fee price based on total amount"""
        prices = [{'amount': 0, 'price': 800},
                  {'amount': 999, 'price': 800},
                  {'amount': 1000, 'price': 400},
                  {'amount': 1999, 'price': 400},
                  {'amount': 2000, 'price': 0},
                  {'amount': 99999, 'price': 0}]
        for p in prices:
            with self.subTest():
                price = p['price']
                result = DeliveryFee.get_by_total_amount(p['amount']).price
                self.assertEqual(price, result)

    def test_get_by_article(self):
        """Return discount based on article id"""
        result = self.discounts.get_by_article(2)
        self.assertEqual(2, result.article_id)
