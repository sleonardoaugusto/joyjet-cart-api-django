from django.shortcuts import render
from rest_framework import viewsets

from .models import (
    Cart,
)
from joyjet_cart_api.core.serializers import (
    CartSerializer,
)


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
