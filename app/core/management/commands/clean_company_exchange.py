from django.core.management.base import BaseCommand
from app.core.models import Company


class Command(BaseCommand):
    help = ('Clean company: Change None exchanges to US')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        companies = Company.objects.filter(exchange_id__isnull=True)

        for company in companies.iterator():
            company.exchange_id = 8
            company.save()
