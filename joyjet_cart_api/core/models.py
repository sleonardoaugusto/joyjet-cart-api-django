from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(null=True)


class Cart(models.Model):
    pass


class Item(models.Model):
    quantity = models.IntegerField(null=False)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
