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
@user_passes_test(lambda u: u.is_staff)
def user(request, username):
    user = LdapUser.objects.filter(username=username).first()
    if not user:
        return redirect('users')
    #print 'photo', user.photo
    form = UserForm(
        instance=user,
        initial= {
            'group': LdapGroup.objects.filter(
                gid=unicode(user.group)
            ).first(),
            'groups': LdapGroup.objects.filter(
                usernames__contains=unicode(user.username)
            ).all(),
            'enable_samba': False,
            'auto_uid': True,
            'auto_home': user.home_directory == make_home_path(user),
            'auto_email': user.email == make_email_adress(user),
        }
    )
    update_password_form = UpdatePasswordForm()
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=user)
        if not form.is_valid():
            print form.data
            print form.errors
        if form.is_valid():
            print "valid!"
            user = form.save(commit=False)
            user.save()
            return redirect('user', user.username)
    context = {
        'user': user,
        'form': form,
        'update_password_form': update_password_form,
    }
    return render(request, 'user.html', context)

@login_required
@user_passes_test(lambda u: u.is_staff)
def group(request, name):
    group = LdapGroup.objects.filter(name=name).first()
    if not group:
        return redirect('groups')
    form = GroupForm(
        instance=group,
        initial= {
            'auto_gid': True,
        }
    )
    if request.method == 'POST':
        form = GroupForm(data=request.POST, instance=group)
        if not form.is_valid():
            print form.data
            print form.errors
        if form.is_valid():
            print "valid!"
            form.save()
            return redirect('group', group.gid)
    context = {
        'group': group,
        'form': form,
    }
    return render(request, 'group.html', context)
