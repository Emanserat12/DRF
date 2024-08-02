import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField()
    inStock = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    category = models.CharField(max_length=255, unique=True, null=False)
    is_removed = models.BooleanField(default=False)

    class Meta:
        db_table = "products"


class Order(models.Model):
    orderId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderedAt = models.BigIntegerField()
    productId = models.ForeignKey(Products, on_delete=models.CASCADE)
    noOfItems = models.IntegerField()
    totalBill = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    is_removed = models.BooleanField(default=False)

    class Meta:
        db_table = "order"
