from django.contrib import admin
from Shop.models import Product, Order, ClientAdress

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(ClientAdress)
