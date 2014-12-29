try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from ldap_manager.api import UserResource, GroupResource, AjaxSearchResource
from tastypie.api import Api

rest_api = Api(api_name="v1")
rest_api.register(AjaxSearchResource())

#user_resource = UserResource()
#group_resource = GroupResource()

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'ldap_manager.views.index', name='index'),
    url(r'^users/', 'ldap_manager.views.users', name='users'),
    url(r'^groups/', 'ldap_manager.views.groups', name='groups'),
    url(r'^add_user/', 'ldap_manager.views.add_user', name='add_user'),
    url(r'^add_group/', 'ldap_manager.views.add_group', name='add_group'),
    url(r'^change_password/(?P<uid>\w{0,50})/$', 'ldap_manager.views.change_password', name='change_password'),
    url(r'^user/(?P<username>\w{0,50})/$', 'ldap_manager.views.user', name='user'),
    url(r'^group/(?P<name>\w{0,50})/$', 'ldap_manager.views.group', name='group'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(rest_api.urls)),

)
