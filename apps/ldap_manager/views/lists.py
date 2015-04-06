from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.ldap_manager.models import LdapGroup, LdapUser, LdapOrgUnit
from apps.ldap_manager.forms import *
from lineage.settings import DEFAULT_HOME, DEFAULT_EMAIL
from string import Template
from django_tables2 import RequestConfig
from apps.ldap_manager.tables import UsersTable, GroupsTable
from apps.ldap_manager.views.util import make_home_path, make_email_adress

@login_required
@user_passes_test(lambda u: u.is_staff)
def users(request):
    table = UsersTable(LdapUser.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'users.html', {'table':table})

@login_required
@user_passes_test(lambda u: u.is_staff)
def groups(request):
    table = GroupsTable(LdapGroup.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'groups.html', {'table': table})

