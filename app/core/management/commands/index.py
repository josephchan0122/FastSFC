import pandas as pd
import os
import sys
import base64
import subprocess
import urllib.request
import urllib.error
import urllib.parse
import traceback
from multiprocessing import Pool
from elasticsearch_dsl import connections
import elasticsearch
import certifi

from django.core.management.base import BaseCommand
from django.conf import settings
from app.core.models import Document
from app.core.helpers.s3 import S3
from app.core.elastic import ESDocument


def index(doc):
    try:
        # Get the URL of the main document depending on exchange
        ex = doc.company.exchange_id
        if ex == 1:
            input_url = doc.url
        elif ex == 5 or ex == 6 or ex == 7 or ex == 8:
            input_url = doc.meta['1']['cached_url']

        # Start indexing
        print('Indexing {}'.format(input_url))

        input_file = urllib.request.urlopen(input_url, timeout=300)
        data = input_file.read()
        body = base64.b64encode(data)

        cat_name = None
        cat_type = None

        if doc.cat:
            cat_name = doc.cat.name
            cat_type = doc.cat.type

        search_doc = ESDocument.get(id=doc.id)
        search_doc.update(
            ticker=doc.company.ticker,
            created_at=doc.date,
            description=doc.description,
            cat=cat_name,
            body=body,
            size=doc.size,
            type=cat_type,
            url=doc.url,
        )
    except elasticsearch.NotFoundError:
        search_doc = ESDocument(
            id=doc.id,
            ticker=doc.company.ticker,
            created_at=doc.date,
            description=doc.description,
            cat=cat_name,
            body=body,
            size=doc.size,
            type=cat_type,
            url=doc.url,
        )
        search_doc.save(pipeline='attachment')
    except Exception as e:
        print('{}.{}: {}'.format(doc.company.ticker, doc.id, e))
        traceback.print_exc()

    doc.indexed = Document.SUCCESS
    doc.save()


class Command(BaseCommand):
    help = ('Index documents for ticker')

    def add_arguments(self, parser):
        parser.add_argument('-t', '--ticker', help='Ticker', required=False)
        parser.add_argument('-r', '--reindex', help='Reindex', action='store_true')

    def handle(self, *args, **options):
        ticker = options['ticker']
        reindex = options['reindex']

        docs = Document.objects.filter(
            company__ticker=ticker,
            meta__isnull=False
        )

        for doc in docs.iterator():
            try:
                if reindex or doc.indexed == Document.NOT_STARTED:
                    index(doc)
            except Exception as e:
                traceback.print_exc()
