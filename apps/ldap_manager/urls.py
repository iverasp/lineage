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
    url(r'^$', 'index.index', name='index'),
    url(r'^initial/', 'index.initial', name='initial'),
    url(r'^users/', 'lists.users', name='users'),
    url(r'^groups/', 'lists.groups', name='groups'),
    url(r'^add/user/', 'add.add_user', name='add_user'),
    url(r'^add/group/', 'add.add_group', name='add_group'),
    url(r'^change_password/(?P<uid>\w{0,50})/$', 'edit.change_password', name='change_password'),
    url(r'^edit/user/(?P<username>\w{0,50})/$', 'edit.user', name='user'),
    url(r'^edit/group/(?P<name>\w{0,50})/$', 'edit.group', name='group'),
    url(r'^detail/user/(?P<username>\w{0,50})/$', 'detail.user', name='user'),
    url(r'^detail/group/(?P<name>\w{0,50})/$', 'detail.group', name='group'),
    url(r'^api/', include(rest_api.urls)),
    url(r'^api/', include(rest_api.urls)),

)
