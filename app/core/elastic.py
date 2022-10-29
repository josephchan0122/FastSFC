import certifi

from django.conf import settings
from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections, analyzer


# Connect to ES
es = connections.create_connection(
    hosts=[settings.ES_HOST],
    http_auth=(settings.ES_USER, settings.ES_PASSWORD),
    use_ssl=settings.ES_USE_SSL,
    ca_certs=certifi.where(),
)

html = analyzer('html',
                tokenizer='standard',
                filter=['standard', 'lowercase', 'stop', 'snowball'],
                char_filter=["html_strip"]
                )


class ESDocument(Document):
    id = Integer()
    body = Text(analyzer=html)
    cat = Text()
    created_at = Date()
    description = Text()
    size = Integer()
    ticker = Text()
    type = Text()
    url = Text()

    class Index:
        name = 'document'
