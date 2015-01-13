try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url
from django.contrib import admin
from api import UserResource, GroupResource, AjaxSearchResource
from tastypie.api import Api

rest_api = Api(api_name="v1")
rest_api.register(AjaxSearchResource())

#user_resource = UserResource()
#group_resource = GroupResource()

admin.autodiscover()

urlpatterns = patterns(
    'apps.ldap_manager.views',
    url(r'^$', 'index', name='index'),
    url(r'^initial/', 'initial', name='initial'),
    url(r'^users/', 'users', name='users'),
    url(r'^groups/', 'groups', name='groups'),
    url(r'^add_user/', 'add_user', name='add_user'),
    url(r'^add_group/', 'add_group', name='add_group'),
    url(r'^change_password/(?P<uid>\w{0,50})/$', 'change_password', name='change_password'),
    url(r'^user/(?P<username>\w{0,50})/$', 'user', name='user'),
    url(r'^group/(?P<name>\w{0,50})/$', 'group', name='group'),
    url(r'^api/', include(rest_api.urls)),

)
