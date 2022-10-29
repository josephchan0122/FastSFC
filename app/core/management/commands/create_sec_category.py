import pandas as pd
import traceback

from django.core.management.base import BaseCommand
from app.core.models import DocumentCategory


class Command(BaseCommand):
    help = ('Create SEC document categories')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            df = pd.read_csv('./app/core/management/commands/sec_category.csv')

            for index, row in df.iterrows():
                DocumentCategory.objects.update_or_create(
                    name=row['name'],
                    defaults={
                        "type": row['type'],
                        "description": row['description'],
                    }
                )
        except Exception as e:
            traceback.print_exc()
