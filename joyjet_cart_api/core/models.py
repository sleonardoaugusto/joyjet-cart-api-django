from django.db import models
from django.db.models import Q


class Article(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True)


class Cart(models.Model):
    pass

    @staticmethod
    def get_amount(items):
        return sum(item.item_amount for item in items)

    @staticmethod
    def get_delivery_fee(total_amount):
        return DeliveryFee.get_by_total_amount(total_amount).price

    @property
    def cart_amount(self):
        total_amount = self.get_amount(self.items.all())
        tax = self.get_delivery_fee(total_amount)
        return total_amount + tax


class Item(models.Model):
    quantity = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

    @property
    def item_amount(self):
        return self.quantity * self.article.price


class DeliveryFee(models.Model):
    min_price = models.IntegerField()
    max_price = models.IntegerField(null=True)
    price = models.IntegerField()

    @classmethod
    def get_by_total_amount(cls, total_amount):
        delivery_fees = cls.objects.all()
        return delivery_fees.get(
            Q(min_price__lte=total_amount),
            Q(max_price__gte=total_amount) | Q(max_price__isnull=True)
        )
