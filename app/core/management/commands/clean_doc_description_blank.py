from django.core.management.base import BaseCommand
from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean document descriptions: Change blank to [Untitled]')

    def handle(self, *args, **options):
        docs = Document.objects.filter(
            description='',
            company__exchange_id__in=[5, 6, 7, 8]
        )

        for doc in docs:
            print(doc.id)
            doc.description = '[Untitled]'
            doc.save()

        print('Done')
