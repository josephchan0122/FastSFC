from django.contrib.sitemaps import Sitemap, GenericSitemap
from app.core.models import Company
from django.core.urlresolvers import reverse


class StaticViewSitemap(Sitemap):
    priority = 1.0

    def items(self):
        return ['core:index']

    def location(self, item):
        return reverse(item)


company_urls = GenericSitemap({'queryset': Company.objects.all()}, priority=1)

sitemaps = {
    'static': StaticViewSitemap,
    'companies:': company_urls,
}
