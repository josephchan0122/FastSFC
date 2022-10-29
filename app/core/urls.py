from django.contrib.sitemaps.views import sitemap
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib import admin
from app.core.views import CompanyDocumentCategorized, CompanyDocumentChrono, CompanyDocumentWebsite, CompanyDocumentSearch, CompanySearch, Ipos, ProfitWarnings, DiscloseableTransactions, Dividends, Earnings, DocumentDetail, WebsiteDocumentDetail, Settings
from app.core.sitemaps import sitemaps

admin.autodiscover()

urlpatterns = [
    # index
    url(r'^$', ensure_csrf_cookie(TemplateView.as_view(template_name='core/index.html')), name='index'),

    # app
    url(r'^company/chronological/(?P<ticker>[a-zA-Z0-9_.-]*)/?$', CompanyDocumentChrono.as_view(), name='company_document_chronological'),
    url(r'^company/website/(?P<ticker>[a-zA-Z0-9_.-]*)/?$', CompanyDocumentWebsite.as_view(), name='company_website_document'),
    url(r'^company/(?P<ticker>[a-zA-Z0-9_.-]*)/?$', CompanyDocumentCategorized.as_view(), name='company_document_categorized'),
    url(r'^company/(?P<ticker>[a-zA-Z0-9_.-]*)/search/?$', CompanyDocumentSearch.as_view(), name='company_document_search'),
    url(r'^document/(?P<id>[a-zA-Z0-9_.-]*)/?$', DocumentDetail.as_view(), name='document_detail'),
    url(r'^document/website/(?P<id>[a-zA-Z0-9_.-]*)/?$', WebsiteDocumentDetail.as_view(), name='website_document_detail'),
    url(r'^search/?$', CompanySearch.as_view(), name='company_search'),

    # leaderboards
    url(r'^recent-ipos/?$', Ipos.as_view(), name='ipos'),
    url(r'^recent-profit-warnings/?$', ProfitWarnings.as_view(), name='profit_warnings'),
    url(r'^recent-discloseable-transactions/?$', DiscloseableTransactions.as_view(), name='discloseable_transactions'),
    url(r'^recent-earnings/?$', Earnings.as_view(), name='earnings'),
    url(r'^recent-dividends/?$', Dividends.as_view(), name='dividends'),

    # private
    url(r'^settings/?$', Settings.as_view(), name='settings'),

    # sitemap
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]
