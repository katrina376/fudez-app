import json

from datetime import date

from django.core.management.base import BaseCommand, CommandError
from account.models import Department
from budget.models import *

class Command(BaseCommand):
    help = 'Initialize the budget in the database.'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **kwargs):
        budget_file = kwargs['file'][1]

        with open(budget_file, 'rb') as jsonfile:
            books = json.loads(jsonfile.read())

        session = Session.objects.create(
                name='106學年度第一期間',
                start_date=date(2017,9,18),
                end_date=date(2018,1,13),
            )

        for book in books:
            b = Book.objects.create(
                    session=session,
                    name=book['name'],
                    description=book['description'],
                    is_active=book['is_active'],
                    announce_date=date(2017,9,26),
                )
            for department in book['departments']:
                d = Department.objects.get(pk=department['id'])
                for project in department['projects']:
                    p = Project.objects.create(
                            book=b,
                            department=d,
                            name=project['name'],
                        )
                    for subject in project['subjects']:
                        s = Subject.objects.create(
                                project=p,
                                name=subject['name'],
                                kind=subject['kind'],
                                is_reserves=subject['is_reserves'],
                            )
                        for item in subject['items']:
                            i = Item.objects.create(
                                    subject=s,
                                    name=item['name'],
                                    estimated_amount=item['estimated_amount'],
                                    memo=item['memo'],
                                    addition=item['addition'],
                                )
