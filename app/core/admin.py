from datetime import datetime, timedelta

from django.contrib import admin
from app.core.models import *
from django.utils.translation import ugettext_lazy as _
from django.db.models import Count, F


class DocumentSummary(Document):
    class Meta:
        proxy = True
        verbose_name = 'Document Summary'
        verbose_name_plural = 'Document Summary'


@admin.register(DocumentSummary)
class DocumentSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/document_summary.html'

    def changelist_view(self, request, extra_context=None):
        response = super(DocumentSummaryAdmin, self).changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        hk = qs.filter(company__exchange_id=1)
        us = qs.filter(company__exchange_id__in=[5, 6, 7, 8])

        hk_total = hk.count()
        us_total = us.count()
        total = qs.count()
        others_total = total - us_total - hk_total

        response.context_data['summary'] = [
            {'key': 'HK', 'value': hk_total},
            {'key': 'US', 'value': us_total},
            {'key': 'Others', 'value': others_total},
            {'key': 'Total', 'value': total},
        ]

        one_month_ago = datetime.today() - timedelta(days=30)

        response.context_data['us_summary'] = us.filter(date__gte=one_month_ago) \
            .extra({'date': "date(date)"}) \
            .values('date') \
            .annotate(date_count=Count('id')) \
            .order_by('-date')

        response.context_data['hk_summary'] = hk.filter(date__gte=one_month_ago) \
            .extra({'date': "date(date)"}) \
            .values('date') \
            .annotate(date_count=Count('id')) \
            .order_by('-date')

        return response


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ["short_name"]


@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(DocumentSubcategory)
class DocumentSubcategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Exchange)
class ExchangeAdmin(admin.ModelAdmin):
    list_display = ["short_name", "full_name"]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["ticker", "full_name", "short_name", "website_url", "exchange", "last_updated"]
    list_filter = ("exchange__short_name",)
    search_fields = ["ticker", "full_name"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["company", "date", "document_url", "cat", "description", "size", "filetype"]
    list_filter = ("cat__type", "company__exchange__short_name")
    search_fields = ["company__ticker", "company__full_name"]

    def document_url(self, doc):
        if doc.url:
            return '<a href="%s">%s</a>' % (doc.url, doc.url)
        else:
            return ''

    document_url.allow_tags = True


class IncompleteFilingFilter(admin.SimpleListFilter):
    """
    DocumentCount - Filter
    Selects tickers that have an complete/incomplete set of filings (i.e. our_count < actual_count)
    https://docs.djangoproject.com/en/dev/ref/contrib/admin/
    Human-readable title which will be displayed in the
    right admin sidebar just above the filter options.
    """
    title = _('complete / incomplete filings')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'filter_tickers'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        return (
            ('complete', _('Complete')),
            ('incomplete', _('Incomplete')),
        )

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        if self.value() == 'complete':
            return queryset.filter(actual_count=F('our_count'))
        elif self.value() == 'incomplete':
            return queryset.exclude(actual_count=F('our_count'))


def refresh_document_count(modeladmin, request, queryset):
    """
    DocumentCount - Action
    Updates internal document count
    """
    for obj in queryset:
        count = Document.objects.filter(company__ticker=obj.company.ticker).count()
        obj.our_count = count
        obj.save()


@admin.register(DocumentCount)
class DocumentCountAdmin (admin.ModelAdmin):
    list_display = ["company", "actual_count", "our_count"]
    list_filter = (IncompleteFilingFilter,)
    actions = [refresh_document_count]
