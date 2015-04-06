from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from apps.ldap_manager.models import LdapGroup, LdapUser, LdapOrgUnit
from apps.ldap_manager.forms.group import *
from apps.ldap_manager.forms.user import *
from lineage.settings import DEFAULT_HOME, DEFAULT_EMAIL
from string import Template
from django_tables2 import RequestConfig
from apps.ldap_manager.tables import UsersTable, GroupsTable
from apps.ldap_manager.views.util import make_home_path, make_email_adress

@login_required
@user_passes_test(lambda u: u.is_staff())
def initial(request):

    if not LdapOrgUnit.objects.filter(name="groups"):
        groups = LdapOrgUnit(name="groups")
        groups.save()
        print "made node groups"

    if not LdapOrgUnit.objects.filter(name="people"):
        print "yolo"
        groups = LdapOrgUnit(name="people")
        groups.save()
        print "made node people"

    return render(request, "initial.html")

def index(request):
    return render(request, 'index.html')



@login_required
@user_passes_test(lambda u: u.is_staff)
def sudoers(request):
    pass

@login_required
@user_passes_test(lambda u: u.is_staff)
def settings(request):
    form = SettingsForm()
    context = {
        'form': form,
    }
    return render(request, 'settings.html', context)

