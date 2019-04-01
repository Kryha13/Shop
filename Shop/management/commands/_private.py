from faker import Factory
import random
from Shop.models import Product, User, ClientAdress


def create_products():
    fake = Factory.create("en_GB")
    for i in range(1, 100):
        Product.objects.create(name=fake.word(), producer=fake.company(), description=fake.paragraph(nb_sentences=3),
                               price=random.randint(1, 10000)/100)


def create_adress():
    fake = Factory.create("en_GB")
    users = User.objects.filter(groups__name='Customers')
    for user in users:
        if ClientAdress.objects.filter(client=user).exists():
            pass
        else:
            ClientAdress.objects.create(client=user, company=fake.company(), street=fake.street_name(),
                                        house_number=random.randint(1, 100), local_number=random.randint(1, 100),
                                        postal_code=fake.postcode(), city=fake.city())
