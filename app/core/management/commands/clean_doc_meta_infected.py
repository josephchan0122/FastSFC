from django.core.management.base import BaseCommand

from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean meta attribute for US filings')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        docs = Document.objects.filter(
            company__exchange_id__in=[5, 6, 7, 8],
            meta__isnull=False,
        )

        for doc in docs.iterator():
            for key in list(doc.meta):
                if not key.isdigit():
                    del doc.meta[key]

            doc.save()

        print('Done')
