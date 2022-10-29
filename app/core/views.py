import math
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic import View, ListView
from django.shortcuts import render
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from app.core.models import Company, Document, WebsiteDocument
from app.core.elastic import ESDocument


class CompanyDocumentCategorized(ListView):
    def get(self, request, ticker):
        try:
            if ticker.isdigit():
                company = Company.objects.get(id=ticker)
            else:
                company = Company.objects.get(ticker=ticker)

            if not Document.objects.filter(company=company).exists():
                return render(request, 'core/company_document.html', {
                    'ticker': ticker,
                    'company': company,
                    'empty': True,
                })

            financials = Document.objects.filter(
                company=company,
                cat__type='financials'
            ).order_by('-date')[:9]

            announcements = Document.objects.filter(
                company=company,
                cat__type='announcements'
            ).order_by('-date')[:9]

            prospectuses = Document.objects.filter(
                company=company,
                cat__type='prospectuses'
            ).order_by('-date')[:9]

            proxies = Document.objects.filter(
                company=company,
                cat__type='proxies'
            ).order_by('-date')[:9]

            ownership = Document.objects.filter(
                company=company,
                cat__type='ownership'
            ).order_by('-date')[:9]

            others = Document.objects.filter(
                company=company,
                cat__type='other'
            ).order_by('-date')[:9]

            return render(request, 'core/company_document.html', {
                'ticker': ticker,
                'company': company,
                'empty': False,
                'financials': financials[:8],
                'financials_count': len(financials),
                'announcements': announcements[:8],
                'announcements_count': len(announcements),
                'prospectuses': prospectuses[:8],
                'prospectuses_count': len(prospectuses),
                'proxies': proxies[:8],
                'proxies_count': len(proxies),
                'ownership': ownership[:8],
                'ownership_count': len(ownership),
                'others': others[:8],
                'others_count': len(others),
            })
        except Company.DoesNotExist:
            return render(request, 'core/company_404.html', {
                'ticker': ticker,
            })


class CompanyDocumentChrono(View):
    def get(self, request, ticker):
        try:
            if ticker.isdigit():
                company = Company.objects.get(id=ticker)
            else:
                company = Company.objects.get(ticker=ticker)

            documents = Document.objects.filter(
                company=company,
            ).order_by('-date')

            return render(request, 'core/company_document_chrono.html', {
                'ticker': ticker,
                'company': company,
                'count': documents.count,
                'documents': documents[:20]
            })
        except Company.DoesNotExist:
            return render(request, 'core/company_404.html', {
                'ticker': ticker,
            })


class CompanyDocumentWebsite(View):
    def get(self, request, ticker):
        try:
            if ticker.isdigit():
                company = Company.objects.get(id=ticker)
            else:
                company = Company.objects.get(ticker=ticker)

            documents = WebsiteDocument.objects.filter(
                company__ticker=ticker,
            ).order_by('-last_updated')

            return render(request, 'core/company_website_document.html', {
                'ticker': ticker,
                'company': company,
                'count': documents.count,
                'documents': documents[:20]
            })
        except Company.DoesNotExist:
            return render(request, 'core/company_404.html', {
                'ticker': ticker,
            })


class CompanyDocumentSearch(View):
    def get_pagination(self, page, total_pages):
        has_prev = True if page > 1 else False
        has_next = True if page < total_pages else False
        start = max(page - 5, 1)
        end = min(page + 4, total_pages)

        pagination = []

        if has_prev:
            pagination.append({
                'label': 'Previous',
                'url': self.url + '?q={}&p={}'.format(self.query, self.page - 1),
            })

        for i in range(start, end + 1):
            pagination.append({
                'label': i,
                'url': self.url + '?q={}&p={}'.format(self.query, i),
            })

        if has_next:
            pagination.append({
                'label': 'Next',
                'url': self.url + '?q={}&p={}'.format(self.query, self.page + 1),
            })

        return pagination

    def get(self, request, ticker):
        self.url = reverse('core:company_document_search', kwargs={'ticker': ticker})
        self.query = request.GET.get('q', None)
        self.page = int(request.GET.get('p', 1))

        if not self.query:
            return HttpResponseRedirect(reverse('core:company_document', kwargs={'ticker': ticker}))

        idx_from = (self.page - 1) * 10
        idx_to = self.page * 10 - 1

        s = ESDocument.search()
        s = s.sort('-created_at').query(
            'match',
            ticker=ticker
        ).query(
            'match',
            attachment=self.query
        ).highlight(
            'body',
            fragment_size=150,
            number_of_fragments=5
        )
        results = s[idx_from:idx_to].execute()

        total_hits = results.hits.total
        total_pages = int(math.ceil(total_hits / 10.0))
        pages = self.get_pagination(self.page, total_pages)

        c = Company.objects.get(ticker=ticker)

        return render(request, 'core/company_document_search.html', {
            'company': c,
            'page': self.page,
            'pages': pages,
            'query': self.query,
            'results': results,
            'ticker': ticker,
            'total_hits': total_hits,
        })


class CompanySearch(View):
    def get(self, request):
        params = request.GET
        query = params['q']

        companies = Company.objects.filter(
            Q(short_name__icontains=query) | Q(ticker__startswith=query)
        )

        return render(request, 'core/search.html', {
            'query': query,
            'results': len(companies),
            'companies': companies,
        })


class Ipos(View):
    def get(self, request):
        one_month_ago = datetime.now() - timedelta(days=30)

        data = Document.objects.filter(
            cat__name__in=[
                'S-1',
                'F-1',
                'S-1/A',
                'F-1/A',
                'Application Proofs and Post Hearing Information Packs or PHIPs'
            ],
            date__gte=one_month_ago,
            company__ticker__isnull=True
        ).order_by('-date')

        return render(request, 'core/leaderboards/ipos.html', {
            'data': data,
        })


class ProfitWarnings(View):
    def get(self, request):
        one_month_ago = datetime.now() - timedelta(days=30)

        data = Document.objects.filter(
            description__contains='Profit Warning',
            date__gte=one_month_ago,
        ).order_by('-date')

        return render(request, 'core/leaderboards/profit_warnings.html', {
            'data': data,
        })


class Earnings(View):
    def get(self, request):
        one_week_ago = datetime.now() - timedelta(days=7)

        data = Document.objects.filter(
            Q(cat__type="financials"),
            Q(date__gte=one_week_ago),
        ).order_by('-date')

        return render(request, 'core/leaderboards/earnings.html', {
            'data': data,
        })


class Dividends(View):
    def get(self, request):
        one_week_ago = datetime.now() - timedelta(days=7)

        data = Document.objects.filter(
            Q(description__contains='Dividend') |
            Q(date__gte=one_month_ago),
        ).order_by('-date')

        return render(request, 'core/leaderboards/dividends.html', {
            'data': data,
        })


class DiscloseableTransactions(View):
    def get(self, request):
        one_month_ago = datetime.now() - timedelta(days=30)

        data = Document.objects.filter(
            Q(description__contains='Major Transaction') |
            Q(description__contains='Discloseable Transaction') |
            Q(description__contains='Major and Connected Transaction'),
            Q(date__gte=one_month_ago),
        ).order_by('-date')

        return render(request, 'core/leaderboards/discloseable_transactions.html', {
            'data': data,
        })


class Settings(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'account/settings.html')


class DocumentDetail(View):
    def get(self, request, id):
        doc = Document.objects.get(id=id)

        # US SEC blocks access from iframe, so if document is US
        # and not cached, redirect to SEC website
        if doc.company.layout == 'us' and doc.cached != Document.SUCCESS:
            return HttpResponseRedirect(doc.url)

        return render(request, 'core/document.html', {
            'document': doc,
            'company': doc.company,
        })


class WebsiteDocumentDetail(View):
    def get(self, request, id):
        document = WebsiteDocument.objects.get(id=id)
        company = Company.objects.get(id=document.company_id)

        return render(request, 'core/website_document.html', {
            'document': document,
            'company': company,
        })
