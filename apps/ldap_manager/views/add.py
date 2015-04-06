from django.http import HttpResponse
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
def change_password(request, uid):
    if request.method == 'POST':
        form = UpdatePasswordForm(data=request.POST)
        if form.is_valid():
            user = LdapUser.objects.filter(uid=uid).first()
            user.set_password(form.cleaned_data.get('password'))
            user.save()
            return redirect('user', user.uid)
    else:
        return redirect('user', uid)

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        print form.data
        if not form.is_valid():
            print form.errors
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('user', user.uid)
    context = {
        'form': form,
    }
    return render(request, 'user.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def add_group(request):
    form = GroupForm()
    if request.method == 'POST':
        form = GroupForm(data=request.POST)
        if not form.is_valid():
            print form.errors
        if form.is_valid():
            print "valid!"
            group = form.save(commit=False)
            group.save()
            return redirect('group', group.gid)
    context = {
        'form': form,
    }
    return render(request, 'group.html', context)
