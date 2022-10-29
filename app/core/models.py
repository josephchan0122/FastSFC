import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.template import Context
from django.template.loader import get_template
from html2text import html2text
from jsonfield import JSONField

from app.core.helpers.emails import send_mass_html_mail


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    meta = JSONField(null=True)


class Watchlist(models.Model):
    company = models.ForeignKey('core.Company', null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    meta = JSONField(null=True)

    class Meta:
        unique_together = ('company', 'user',)


class Period(models.Model):
    short_name = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.short_name


class DocumentCategory(models.Model):
    name = models.CharField(max_length=200, null=False)
    type = models.CharField(max_length=200, null=False, default="other", db_index=True)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Document Categories"


class DocumentSubcategory(models.Model):
    name = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Document Subcategories"


class Exchange(models.Model):
    short_name = models.CharField(max_length=20, null=True)
    full_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.short_name


class Company(models.Model):
    ticker = models.CharField(max_length=10, null=True, db_index=True)
    ticker_alt = models.CharField(max_length=100, null=True)
    exchange = models.ForeignKey('core.Exchange', null=True)
    full_name = models.CharField(max_length=200, null=True)
    full_alt_name = models.CharField(max_length=500, null=True)
    industry = models.ForeignKey('core.Industry', null=True)
    meta = JSONField(null=True)
    short_alt_name = models.CharField(max_length=100, null=True, db_index=True, unique=True)
    short_name = models.CharField(max_length=200, null=True, db_index=True)
    website = models.URLField(null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.ticker or self.short_name

    @property
    def identifier(self):
        return self.ticker or self.id

    @property
    def layout(self):
        if self.exchange.short_name == 'NYSE' \
                or self.exchange.short_name == 'NASDAQ' \
                or self.exchange.short_name == 'AMEX' \
                or self.exchange.short_name == 'US':
            return 'us'

        return 'hk'

    def get_absolute_url(self):
        return reverse('core:company_document', kwargs={'ticker': self.ticker})

    def website_url(self):
        if self.website:
            return '<a href="%s">%s</a>' % (self.website, self.website)
        else:
            return ''

    def get_latest_document(self):
        try:
            return Document.objects.filter(company__ticker=self.ticker).order_by('-date')[0]
        except:
            return None

    def get_document_count(self):
        try:
            return Document.objects.filter(company__ticker=self.ticker).count()
        except:
            return 0

    website_url.allow_tags = True

    class Meta:
        verbose_name_plural = "Companies"


class Document(models.Model):
    FILETYPE_CHOICES = (
        ('pdf', 'pdf'),
        ('html', 'html'),
        ('htm', 'htm'),
        ('ppt', 'ppt'),
        ('doc', 'doc'),
        ('Multiple', 'Multiple'),
    )

    NOT_STARTED = 0
    STARTED = 1
    SUCCESS = 2
    ERROR = 3
    NA = 4
    STATUS_CHOICES = (
        (NOT_STARTED, 'Not started'),
        (STARTED, 'Started'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
    )

    cached_url = models.URLField(null=True)
    cat = models.ForeignKey('core.DocumentCategory', null=True)
    company = models.ForeignKey('core.Company', null=True)
    date = models.DateTimeField(null=True, db_index=True)
    description = models.CharField(max_length=1000, null=True)
    filetype = models.CharField(max_length=20, choices=FILETYPE_CHOICES, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    meta = JSONField(null=True)
    ref = models.CharField(max_length=50, null=True, db_index=True)
    size = models.IntegerField(null=True)
    subcat = models.ForeignKey('core.DocumentSubcategory', null=True)
    url = models.URLField(null=True)

    cached = models.SmallIntegerField(default=0, choices=STATUS_CHOICES, null=False, db_index=True)
    parsed = models.SmallIntegerField(default=0, choices=STATUS_CHOICES, null=False, db_index=True)
    indexed = models.SmallIntegerField(default=0, choices=STATUS_CHOICES, null=False, db_index=True)

    class Meta:
        index_together = (
            ('company', 'cat'),
        )


class WebsiteDocument(models.Model):
    company = models.ForeignKey('core.Company', null=True)
    url = models.URLField(null=True)
    description = models.CharField(max_length=1000, null=True)
    last_updated = models.DateTimeField(auto_now=True)


class DocumentCount(models.Model):
    company = models.ForeignKey('core.Company', null=False)
    actual_count = models.IntegerField(null=True)
    our_count = models.IntegerField(null=True)
    cache_count = models.IntegerField(null=True)
    index_count = models.IntegerField(null=True)

    class Meta:
        verbose_name_plural = "Document Counts"


class Price(models.Model):
    company = models.ForeignKey('core.Company', null=True)
    date = models.DateTimeField(null=True, db_index=True)
    open = models.FloatField(null=True)
    high = models.FloatField(null=True)
    low = models.FloatField(null=True)
    close = models.FloatField(null=True)
    adj_close = models.FloatField(null=True)
    volume = models.FloatField(null=True)


class Industry(models.Model):
    industry = models.CharField(max_length=100, null=True)
    supersector = models.CharField(max_length=100, null=True)
    sector = models.CharField(max_length=100, null=True)
    subsector = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=10, null=True)


class Source(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    description = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.name


class Metric(models.Model):
    name = models.CharField(max_length=255, null=False, unique=True, db_index=True)
    source = models.ForeignKey('core.Source', null=True, default=None)
    description = models.CharField(max_length=1000, null=True)
    type = models.CharField(max_length=20, null=True)
    meta = JSONField(null=True)

    def __str__(self):
        return self.name

    def timeseriesCount(self):
        return Timeseries.objects.filter(metric_id__exact=self.id).count()


class Timeseries(models.Model):
    metric = models.ForeignKey('core.Metric', null=False)
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    type = models.CharField(max_length=20, null=True)
    value = models.FloatField(null=True)
    get_latest_by = 'date'


@receiver(post_save, sender=Document)
def send_alert(sender, instance, created, **kwargs):
    """
    Post-save signal
    """
    if not created:
        # do not continue if it's a modification
        return
    try:
        # precompile template
        template = get_template("emails/document_alert.html")

        users_data = instance.company.watchlist_set.select_related(
            'user', 'company'
        ).values(
            'company__ticker', 'user__username', 'user__email', 'company__short_name'
        )
        emails = []
        host = settings.SITE_HOST
        for user_data in users_data:
            # generate email context
            user_context = {
                "username": user_data['user__username'],
                "company_name": user_data['company__short_name'],
                "company_ticker": user_data['company__ticker'],
                "document_url": host + reverse('core:document_detail', kwargs={'id': instance.id}),
                "document_date": instance.date,
                "document_description": instance.description,
                "company_url": host + reverse(
                    'core:company_document_categorized',
                    kwargs={
                        'ticker': user_data['company__ticker']
                    }
                ),
                "settings_url": host + reverse('core:settings')
            }
            # generate an email
            html_email = template.render(Context(user_context))
            txt_email = html2text(html_email)

            sender = 'FastSFC Alerts <alerts@fastsfc.com>'
            recipient = [user_data['user__email']]
            subject = "{ticker}: {document_description}".format(
                ticker=user_data['company__ticker'],
                document_description=instance.description
            )

            # subject, text, html, from_email, recipient
            emails.append([subject, txt_email, html_email, sender, recipient])
        # send a batch
        send_mass_html_mail(emails, fail_silently=True)

    except Exception as e:
        # do not block saving if there is a problem with emails
        # but log an error
        logging.exception(e)
