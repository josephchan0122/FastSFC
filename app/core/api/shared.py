import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from app.core.models import Metric, Timeseries, Source, Watchlist
from rest_framework import serializers, viewsets, filters
import json


# Serializers
class JSONSerializerField(serializers.Field):
    def to_internal_value(self, data):
        return json.loads(data)

    def to_representation(self, value):
        return value


class SourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Source
        fields = ('name', 'description')


class MetricSerializer(serializers.ModelSerializer):
    timeseries_count = serializers.IntegerField(source='timeseriesCount')
    source = SourceSerializer
    meta = JSONSerializerField()

    class Meta:
        model = Metric
        fields = ('id', 'name', 'timeseries_count', 'source', 'meta')


class TimeseriesSerializer(serializers.ModelSerializer):
    metric = MetricSerializer()

    class Meta:
        model = Timeseries
        fields = ('metric', 'start_date', 'end_date', 'type', 'value')

# Filters


class TimeseriesFilter(django_filters.FilterSet):
    class Meta:
        model = Timeseries
        fields = {'metric__name': ['exact', 'icontains'],
                  'metric__id': ['exact'],
                  'start_date': ['exact', 'gte', 'lte'],
                  'end_date': ['exact', 'gte', 'lte']
                  }


class MetricFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(method='filter_meta_ticker')
    company = django_filters.CharFilter(method='filter_meta_company')

    class Meta:
        model = Metric
        fields = ('name', 'description', 'ticker', 'company')

    def filter_meta_ticker(self, queryset, value):
        query = json.dumps({'ticker': value}).replace(" ", "")[1:-1]
        return queryset.filter(meta__icontains=query)

    def filter_meta_company(self, queryset, value):
        query = json.dumps({'company': value}).replace(" ", "")[1:-1]
        return queryset.filter(meta__icontains=query)

# Viewsets


class TimeseriesViewSet(viewsets.ModelViewSet):
    queryset = Timeseries.objects.all()
    serializer_class = TimeseriesSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = TimeseriesFilter
    ordering_fields = ('start_date')
    ordering = ('-start_date')


class MetricViewSet(viewsets.ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    )
    filter_class = MetricFilter
    search_fields = ('$name')
