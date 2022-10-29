import json
import traceback

from django.core.management.base import BaseCommand
from app.core.models import Industry


class Command(BaseCommand):
    help = ('Create ICB industry categories')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            with open('./app/core/management/commands/icb.json') as f:
                data = json.load(f)

                for obj in data:
                    industry = obj['name']

                    for obj in obj['supersectors']:
                        supersector = obj['name']

                        for obj in obj['sectors']:
                            sector = obj['name']

                            for obj in obj['subsectors']:
                                subsector = obj['name']
                                code = obj['icb']

                                print('{}: {}, {}, {}, {}'.format(code, subsector, sector, supersector, industry))

                                Industry.objects.update_or_create(
                                    code=obj['icb'],
                                    defaults={
                                        "industry": industry,
                                        "supersector": supersector,
                                        "sector": sector,
                                        "subsector": subsector,
                                    }
                                )

        except Exception as e:
            traceback.print_exc()
