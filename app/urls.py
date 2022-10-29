from django.conf.urls.static import static
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import logout
from app.core.api.resources import router

admin.autodiscover()

urlpatterns = [
    url(r'^api/v1/', include(router.urls)),

    # core
    url(r'', include('app.core.urls', namespace='core')),

    # log
    url(r'', include('app.log.urls', namespace='log')),

    # django-allauth
    url(r'^logout/$', logout, {'next_page': '/'}),
    url(r'', include('allauth.urls')),

    # admin
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns = staticfiles_urlpatterns() + urlpatterns
    urlpatterns = static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + urlpatterns
