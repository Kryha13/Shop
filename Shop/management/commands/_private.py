from faker import Factory
import random
from Shop.models import Product, Order


def create_products():
    fake = Factory.create("en_GB")
    for i in range(1, 100):
        Product.objects.create(name=fake.word(), producer=fake.company(), description=fake.paragraph(nb_sentences=3),
                               price=random.randint(1, 10000)/100)
