try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'ldap_manager.views.index', name='index'),
    url(r'^users/', 'ldap_manager.views.users', name='users'),
    url(r'^user/(?P<uid>\w{0,50})/$', 'ldap_manager.views.user', name='user'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
