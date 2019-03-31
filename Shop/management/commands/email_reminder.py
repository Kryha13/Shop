import datetime
from django.core.mail import EmailMessage
from django.core.management import BaseCommand
from django.template.loader import render_to_string
from Shop.models import Order


def run():
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


class Command(BaseCommand):

    def handle(self, *args, **options):
        run()
        self.stdout.write(self.style.SUCCESS("Successfully sent reminders"))