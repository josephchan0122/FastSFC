from django.core.management.base import BaseCommand
from app.core.models import Document


class Command(BaseCommand):
    help = ('Clean document descriptions: Fix titlecase')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        docs = Document.objects.all()

        for doc in docs.iterator():
            print(doc.id)
            doc.description = doc.description.replace("'S", "'s")
            doc.description = doc.description.replace("1St", "1st")
            doc.description = doc.description.replace("2Nd", "2nd")
            doc.description = doc.description.replace("3Rd", "3rd")
            doc.description = doc.description.replace("4Th", "4th")
            doc.description = doc.description.replace("5Th", "5th")
            doc.description = doc.description.replace("6Th", "6th")
            doc.description = doc.description.replace("7Th", "7th")
            doc.description = doc.description.replace("8Th", "8th")
            doc.description = doc.description.replace("9Th", "9th")
            doc.description = doc.description.replace("Phip", "PHIP")
            doc.description = doc.description.replace("Us$", "US$")
            doc.save()
