from __future__ import absolute_import, unicode_literals
from celery import task
import datetime
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from Shop.models import Order


@task()
def email_reminder():
    orders = Order.objects.filter(payment_deadline__gte=datetime.date.today())
    for order in orders:
        mail_subject = 'Reminder of payment'
        message = render_to_string('orders/reminder_email.html', {
            'user': order.client,
            'deadline': order.payment_deadline,
            'invoice': order.id,
        })
        to_email = order.client.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
