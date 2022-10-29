from django.core.management.base import BaseCommand
from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean document filetype: Standardize filetypes')

    def handle(self, *args, **options):
        docs = Document.objects.all()

        for doc in docs.iterator():
            try:
                # Remove . prefix
                if doc.filetype[0] == '.':
                    doc.filetype = doc.filetype[1:]
                    doc.save()

                # Convert uppercase to lowercase
                if doc.filetype.isupper():
                    doc.filetype = doc.filetype.lower()
                    doc.save()

            except:
                pass

        print('Done')
