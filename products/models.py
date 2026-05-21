from django.db import models
from suppliers.models import Supplier
# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=100)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    min_stock = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.name


    def is_low_stock(self):
        return self.stock < self.min_stock