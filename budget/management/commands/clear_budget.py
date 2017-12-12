from django.core.management.base import BaseCommand, CommandError
from budget.models import *

class Command(BaseCommand):
    help = 'Clear the budget in the database.'

    def handle(self, *args, **kwargs):
        Item.objects.all().delete()
        Subject.objects.all().delete()
        Project.objects.all().delete()
        Book.objects.all().delete()
        Session.objects.all().delete()
