import certifi
import traceback
from elasticsearch import Elasticsearch
from elasticsearch.client.ingest import IngestClient

from django.conf import settings
from django.core.management.base import BaseCommand
from app.core.elastic import ESDocument


class Command(BaseCommand):
    help = ('Update Elasticsearch index')

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        try:
            es = Elasticsearch(
                hosts=[settings.ES_HOST],
                http_auth=(settings.ES_USER, settings.ES_PASSWORD),
                use_ssl=settings.ES_USE_SSL,
                ca_certs=certifi.where(),
            )

            # Delete index
            es.indices.delete(index='document', ignore=[400, 404])

            # Create ingest attachment pipeline
            IngestClient(es).put_pipeline(id='attachment', body={
                'description': 'Extract text from files with Tika',
                'processors': [{
                    'attachment': {'field': 'body'}
                }]
            })

            # Create index
            ESDocument.init()
        except Exception as e:
            traceback.print_exc()
