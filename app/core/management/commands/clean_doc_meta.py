from django.core.management.base import BaseCommand

from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean meta attribute in documents on HKEx')

    def add_arguments(self, parser):
        parser.add_argument('-t', '--ticker', help='Ticker', required=False)

    def handle(self, *args, **options):
        ticker = options['ticker']

        if ticker:
            docs = Document.objects.filter(
                company__ticker=ticker,
                company__exchange_id=1
            )
        else:
            docs = Document.objects.filter(
                company__exchange_id=1,
                meta__isnull=False,
            )

        for doc in docs:
            print('Clean {} doc id {}'.format(doc.company.ticker, doc.id))
            doc.meta = None
            doc.save()

        print('Done')
