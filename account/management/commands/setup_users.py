import json

from django.core.management.base import BaseCommand, CommandError

from account.models import Department, User


class Command(BaseCommand):
    help = 'Initialize the users in the database.'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        user_file = kwargs['file'][1]

        with open(user_file, 'rb') as jsonfile:
            users = json.loads(jsonfile.read())

        for u in users:
            if not User.objects.filter(username=u['username']).exists():
                try:
                    department = Department.objects.get(name=u['department'])
                    u['department'] = department
                    level = u.pop('level')
                    if level == 'superuser':
                        user = User.objects.create_superuser(**u)
                    else:
                        user = User.objects.create_user(**u)
                except Exception as e:
                    print(e)
                    raise CommandError(
                        'Exception occurs when creating {name}'.format(name=u['name']))
                department.closed = True
