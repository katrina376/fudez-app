import json

from django.core.management.base import BaseCommand, CommandError

from account.models import Department


class Command(BaseCommand):
    help = 'Initialize the departments in the database.'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        department_file = kwargs['file'][1]

        with open(department_file, 'rb') as jsonfile:
            departments = json.loads(jsonfile.read())

        for d in departments:
            if not Department.objects.filter(name=d['name']).exists():
                try:
                    department = Department.objects.create(**d)
                except:
                    raise CommandError(
                        'Exception occurs when creating {name}'.format(name=d['name']))
                department.closed = True
