from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True)


class Cart(models.Model):
    pass

    @property
    def cart_amount(self):
        return sum(item.item_amount for item in self.items.all())


class Item(models.Model):
    quantity = models.IntegerField(null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)

    @property
    def item_amount(self):
        return self.quantity * self.article.price
