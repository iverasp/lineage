from django.http import HttpResponse, HttpResponseNotFound
from django.template import RequestContext
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.ldap_manager.models import LdapGroup, LdapUser, LdapOrgUnit
from apps.ldap_manager.forms.user import *
from apps.ldap_manager.forms.group import *
from lineage.settings import DEFAULT_HOME, DEFAULT_EMAIL
from string import Template
from django_tables2 import RequestConfig
from apps.ldap_manager.tables import UsersTable, GroupsTable
from apps.ldap_manager.views.util import make_home_path, make_email_adress

@login_required
@user_passes_test(lambda u: u.is_staff)
def user(request, username=None):
    if username:
        user = LdapUser.objects.filter(username=username).first()
        return render(request, 'detail/user.html', {'u': user })

    return HttpResponseNotFound()


@login_required
@user_passes_test(lambda u: u.is_staff)
def group(request, groupname=None):
    if groupname:
        user = LdapGroup.objects.filter(name=groupname).first()
        return render(request, 'detail/group.html', {'g': groupname })

    return HttpResponseNotFound()

