from django.core.management.base import BaseCommand
from  Shop.management.commands._private import create_products


class Command(BaseCommand):

    def handle(self, *args, **options):
        create_products()
        self.stdout.write(self.style.SUCCESS("Successfully created Products"))