from django.contrib.auth.models import User
from django.db.models import Case, IntegerField, Value, When
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import pagination, routers
from rest_framework.filters import SearchFilter
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.core.api.shared import *
from app.core.models import (
    Company, Document, DocumentCategory,
    DocumentSubcategory, Exchange, Price, WebsiteDocument
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_staff')


class ExchangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exchange
        fields = ('short_name', 'full_name')


class DocumentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCategory
        fields = ('name', 'type')


class DocumentSubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSubcategory
        fields = ('name',)


class CompanySerializer(serializers.ModelSerializer):
    exchange = serializers.StringRelatedField()

    class Meta:
        model = Company
        fields = ('id', 'ticker', 'full_name', 'short_name', 'exchange', 'layout', 'website')


class WatchlistSerializer(serializers.ModelSerializer):
    meta = JSONSerializerField()
    company = CompanySerializer()
    user = UserSerializer()

    class Meta:
        model = Watchlist
        fields = ('id', 'company', 'user', 'meta')


class DocumentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    cat = DocumentCategorySerializer()
    meta = JSONSerializerField()
    subcat = serializers.StringRelatedField()

    class Meta:
        model = Document
        fields = ('id', 'company', 'cat', 'subcat', 'date', 'description', 'filetype', 'meta', 'size', 'url', 'last_updated')


class WebsiteDocumentSerializer(serializers.ModelSerializer):
    company = CompanySerializer()

    class Meta:
        model = WebsiteDocument
        fields = ('id', 'company', 'description', 'url', 'last_updated')


class PriceSerializer(serializers.ModelSerializer):
    company = serializers.StringRelatedField()

    class Meta:
        model = Price
        fields = ('company', 'date', 'open', 'close', 'high', 'low', 'adj_close', 'volume')


class PriceFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(field_name='company__ticker')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')

    class Meta:
        model = Price
        fields = ('company', 'date', 'open', 'close', 'high', 'low', 'adj_close', 'volume')


class DocumentFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(field_name='company__ticker')
    type = django_filters.CharFilter(field_name='cat__type')
    date_from = django_filters.DateFilter(field_name='date', lookup_expr='gte')

    class Meta:
        model = Document
        fields = ('ticker', 'cat', 'subcat', 'date', 'description', 'filetype', 'size', 'url', 'last_updated')


class WebsiteDocumentFilter(django_filters.FilterSet):
    ticker = django_filters.CharFilter(field_name='company__ticker')
    type = django_filters.CharFilter(field_name='cat__type')

    class Meta:
        model = WebsiteDocument
        fields = ('ticker', 'description', 'url', 'last_updated')


class RelevantSearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):
        queryset = super(RelevantSearchFilter, self).filter_queryset(request, queryset, view)
        search_value = request.query_params.get('search')

        if not search_value:
            return queryset

        return queryset.annotate(
            custom_order=Case(
                When(ticker=search_value, then=Value(8)),
                When(short_name=search_value, then=Value(7)),
                When(ticker__istartswith=search_value, then=Value(6)),
                When(ticker__iendswith=search_value, then=Value(5)),
                When(ticker__icontains=search_value, then=Value(4)),
                When(short_name__istartswith=search_value, then=Value(3)),
                When(short_name__iendswith=search_value, then=Value(2)),
                When(short_name__icontains=search_value, then=Value(1)),
                output_field=IntegerField(),
            )
        ).order_by('-custom_order')


class PricePagination(pagination.LimitOffsetPagination):
    default_limit = 251
    max_limit = 1000


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    lookup_value_regex = '[^/]+'

    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        company = request.data.get('company')
        user = request.user
        meta = request.data.get('meta', {})

        company_filter = self._get_filter(company)
        company_id = get_object_or_404(
            Company.objects.all().values_list('id', flat=True),
            **company_filter
        )

        watching_list, _ = Watchlist.objects.get_or_create(
            user_id=user.id,
            company_id=company_id,
        )

        if watching_list.meta != meta:
            watching_list.meta = meta
            watching_list.save()

        serializer = WatchlistSerializer(watching_list)
        return Response(serializer.data)

    def get_object(self):
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)

        needle = self.kwargs[self.lookup_field]
        filter = self._get_filter(needle, 'company__')

        obj = get_object_or_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)

        return obj

    def _get_filter(self, needle, prefix=''):
        if needle.isdigit():
            return {prefix + 'id': needle}
        else:
            return {prefix + 'ticker': needle}


class ExchangeViewSet(viewsets.ModelViewSet):
    queryset = Exchange.objects.all()
    serializer_class = ExchangeSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = DocumentFilter
    ordering_fields = ('date')
    ordering = ('-date',)


class WebsiteDocumentViewSet(viewsets.ModelViewSet):
    queryset = WebsiteDocument.objects.all()
    serializer_class = WebsiteDocumentSerializer

    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = WebsiteDocumentFilter
    ordering_fields = ('last_updated')
    ordering = ('-last_updated',)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    filter_backends = (RelevantSearchFilter,)
    search_fields = ('ticker', 'short_name')


class PriceViewSet(viewsets.ModelViewSet):
    queryset = Price.objects.all()
    serializer_class = PriceSerializer
    pagination_class = PricePagination

    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filter_class = PriceFilter
    ordering_fields = ('date')
    ordering = ('-date',)


router = routers.DefaultRouter()
router.register('exchange', ExchangeViewSet)
router.register('document', DocumentViewSet)
router.register('website-document', WebsiteDocumentViewSet)
router.register('company', CompanyViewSet)
router.register('price', PriceViewSet)
router.register('metric', MetricViewSet)
router.register('timeseries', TimeseriesViewSet)
router.register('watchlist', WatchlistViewSet, base_name='watchlist')
