from django.core.management.base import BaseCommand

from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean meta text attribute in documents')

    def add_arguments(self, parser):
        pass

    def replace_key(self, doc, from_key, to_key):
        """
        Case insensitive replace on keys
        doc: Document
        from_key: previous key
        to_key: to new key
        """
        if from_key in doc.meta:
            doc.meta[to_key] = doc.meta[from_key]
            del doc.meta[from_key]
            doc.save()

        if from_key.upper() in doc.meta:
            doc.meta[to_key] = doc.meta[from_key.upper()]
            del doc.meta[from_key.upper()]
            doc.save()

    def migrate_indexed(self, doc):
        if 'indexed' in doc.meta:
            doc.indexed = Document.SUCCESS
            del doc.meta['indexed']
            doc.save()

    def handle(self, *args, **options):
        docs = Document.objects.filter(
            meta__isnull=False,
        )

        for doc in docs.iterator():
            self.migrate_indexed(doc)
            self.replace_key(doc, 'text', 'txt')
            self.replace_key(doc, '.txt', 'txt')
            self.replace_key(doc, '.pdf', 'pdf')
            self.replace_key(doc, '.htm', 'html')
            self.replace_key(doc, '.doc', 'doc')

        print('Done')
