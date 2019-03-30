from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

import datetime

# Create your models here.


def deadline():
    return datetime.date.today() + datetime.timedelta(days=20)


class Product(models.Model):
    name = models.TextField(max_length=100)
    producer = models.TextField(max_length=100)
    description = models.TextField()
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='static/', blank=True)
    image_thumbnail = ImageSpecField(source='image',
                                     processors=[ResizeToFill(50, 50)],
                                     format='JPEG',
                                     options={'quality': 60})

    def __str__(self):
        return self.name


class Order(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    # adress = models.ForeignKey()
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

    def __str__(self):
        return self.client.first_name + ' ' + self.client.last_name
