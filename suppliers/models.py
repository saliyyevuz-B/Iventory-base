from django.db import models

# Create your models here.


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name