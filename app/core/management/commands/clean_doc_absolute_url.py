from django.core.management.base import BaseCommand
from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean document descriptions: Fix URL of SEC filings')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        docs = Document.objects.filter(url__startswith='/Archives/edgar/data/')

        for doc in docs.iterator():
            doc.url = 'https://www.sec.gov' + doc.url
            doc.save()
