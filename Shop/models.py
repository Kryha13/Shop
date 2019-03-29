from django.db import models
from django.contrib.auth.models import User

import datetime

# Create your models here.


def deadline():
    return datetime.date.today() + datetime.timedelta(days=20)


class Product(models.Model):
    name = models.TextField(max_length=100)
    producer = models.TextField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/', blank=True)


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ForeignKey(Product, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    payment_deadline = models.DateField(datetime.date.today() + datetime.timedelta(days=7))
    value = models.DecimalField(max_digits=15, decimal_places=2)


class ClientAdress(models.Model):
    client = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.TextField(max_length=100)
    street = models.TextField(max_length=100)
    house_number = models.IntegerField()
    local_number = models.IntegerField()
    postal_code = models.CharField(max_length=5)
    city = models.TextField(max_length=100)


