from pydoc import describe
from django.db import models
from django.utils import timezone
from PIL import Image
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.
class Petrol(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    status = models.CharField(max_length=2,choices=(('1','Active'),('0', 'Inactive')) , default = 1)
    price = models.FloatField(max_length=(15,2), default= 0)
    delete_flag = models.IntegerField(default = 0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Petrol Type List"

    def __str__(self):
        return str(f"{self.name}")

    def available(self):
        try:
            stockin = Stock.objects.filter(petrol = self).aggregate(models.Sum("volume"))['volume__sum']
            if stockin is None:
                stockin = 0
        except:
            stockin = 0
        try:
            sale = Sale.objects.filter(petrol = self).aggregate(models.Sum("volume"))['volume__sum']
            if sale is None:
                sale = 0
        except:
            sale = 0
            print(sale)
        return stockin - sale

class Stock(models.Model):
    date = models.DateField(null=True, blank = True)
    petrol = models.ForeignKey(Petrol, on_delete=models.CASCADE)
    volume = models.FloatField(max_length=(15,2), default=0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "Stock-In Records"

    def __str__(self):
        return f"{self.petrol.name} - [{self.volume} L]"

class Sale(models.Model):
    date = models.DateField(null=True, blank = True)
    customer_name = models.CharField(max_length=250)
    petrol = models.ForeignKey(Petrol, on_delete=models.CASCADE)
    volume = models.FloatField(max_length=(15,2), default=0)
    price = models.FloatField(max_length=(15,2), default=0)
    amount = models.FloatField(max_length=(15,2), default=0)
    date_added = models.DateTimeField(default = timezone.now)
    date_created = models.DateTimeField(auto_now = True)

    class Meta:
        verbose_name_plural = "List of Sales"

    def __str__(self):
        return f"{self.customer_name} - [{self.petrol} - {self.volume} L]"

