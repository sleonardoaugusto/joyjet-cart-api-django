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
    def price(self):
        total_amount = self.get_amount(self.items.all())
        tax = self.get_delivery_fee(total_amount)
        return total_amount + tax


class Item(models.Model):
    quantity = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

    @property
    def item_amount(self):
        discount = Discount.get_by_article(self.article_id)

        if discount:
            net_total = self.apply_discount(discount, self.article.price, self.quantity)
        else:
            net_total = self.quantity * self.article.price

        return net_total

    @staticmethod
    def apply_discount(discount, price, qty):
        total_amount = qty * price

        if discount.disc_type == 'amount':
            disc_amount = discount.value * qty
        else:
            disc_amount = total_amount * discount.value / 100

        return int(total_amount - disc_amount)


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


class Discount(models.Model):
    disc_type = models.TextField('amount percentage')
    value = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    @classmethod
    def get_by_article(cls, article_id):
        return cls.objects.filter(article=article_id).first()
