from django.db import models
from products.models import Product
from suppliers.models import Supplier
# Create your models here.


class StockIn(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField()
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.product.name} -- +{self.quantity}"

    def save(self, *args, **kwargs):
        self.product.stock += self.quantity
        self.product.save()
        super().save(*args, **kwargs)

class StockOut(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    customer_name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} — -{self.quantity}"

    def save(self, *args, **kwargs):
        self.product.stock -= self.quantity
        self.product.save()
        super().save(*args, **kwargs)

























