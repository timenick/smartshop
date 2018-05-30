# Stdlib imports

# Core Django imports
from django.db import models

# Third-party app imports

# Imports from your apps
from categories.models import Category


class Merchandise(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=15)
    barcode = models.CharField(max_length=15, blank=True)
    name = models.CharField(max_length=30, blank=True)
    brand = models.CharField(max_length=10, blank=True)
    originPrice = models.DecimalField(max_digits=8, decimal_places=2)
    scale = models.CharField(max_length=10, blank=True)
    factory = models.CharField(max_length=30, blank=True)
    priceChecker = models.CharField(max_length=10, blank=True)
    supervisionCode = models.CharField(max_length=30, blank=True)
    supervisor = models.CharField(max_length=20, blank=True)
    unit = models.CharField(max_length=10, blank=True)
    supervisorTel = models.CharField(max_length=13, blank=True)
    promotionPrice = models.DecimalField(max_digits=8, decimal_places=2, default=originPrice)
    clubPrice = models.DecimalField(max_digits=8, decimal_places=2, default=originPrice)
    producePlace = models.CharField(max_length=10, blank=True)
    createTime = models.DateTimeField(auto_now_add=True)
    updateTime = models.DateTimeField(auto_now=True)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)

    # picture = models.ImageField("Uploaded image/MerchandiseImg", upload_to=scramble_uploaded_filename)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('createTime',)