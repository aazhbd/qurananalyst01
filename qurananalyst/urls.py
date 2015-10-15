from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from registration.backends.default.views import RegistrationView
from forms import RegistrationFormCaptcha
import settings
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', 'qurananalyst.views.home', name='home'),
    url(r'^home$', 'qurananalyst.views.home', name='home'),

	url(r'^info$', 'qurananalyst.views.info', name='info'),
    
    url(r'^(?P<chap>\d+)/?$', 'qurananalyst.views.chapter', name='chapter'),
    url(r'^getchapter$', 'qurananalyst.views.getchapter', name='getchapter'),
    
    url(r'^(?P<chap>\d+)/(?P<verse>\d+)/?$', 'qurananalyst.views.verse', name='verse'),
    url(r'^getverse$', 'qurananalyst.views.getverse', name='getverse'),
    
    url(r'^search/(?P<search>.+?)/(?P<page>\d+)/?$', 'qurananalyst.views.search', name='search'),
    url(r'^search/(?P<search>.+?)/?$', 'qurananalyst.views.search', name='search'),
    url(r'^search/?$', 'qurananalyst.views.search', name='search'),
    
    url(r'^discussions$', 'qurananalyst.views.discussions', name='discussions'),
    
    
    # url(r'^qurananalyst/', include('qurananalyst.foo.urls')),
    
    url(r'^accounts/register/$', RegistrationView.as_view(form_class=RegistrationFormCaptcha), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^%s(?P<path>.*)$' % settings.STATIC_URL.lstrip('/'), 'django.contrib.staticfiles.views.serve'),
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'), 'django.views.static.serve', kwargs=dict(document_root=settings.MEDIA_ROOT)),
)
