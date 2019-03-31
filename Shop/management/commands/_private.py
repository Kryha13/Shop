from faker import Factory
import random
from Shop.models import Product, Order
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def create_products():
    fake = Factory.create("en_GB")
    for i in range(1, 100):
        Product.objects.create(name=fake.word(), producer=fake.company(), description=fake.paragraph(nb_sentences=3),
                               price=random.randint(1, 10000)/100)


def send_reminder():
    orders = Order.objects.filter(payment_deadline__gt=datetime.date.today())

    for order in orders:
        mail_subject = 'Reminder of payment'
        message = render_to_string('reminder_email.html', {
            'user': order.client,
            'deadline': order.payment_deadline,
            'invoice': order.id,

        })
        to_email = order.client.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()