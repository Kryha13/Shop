from django.core.management.base import BaseCommand
from  Shop.management.commands._private import create_adress


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_adress()
        self.stdout.write(self.style.SUCCESS("Successfully created Clients adresses"))