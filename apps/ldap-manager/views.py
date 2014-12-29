from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from models import LdapGroup, LdapUser
from forms import *
from django-ldap-manager.settings import DEFAULT_HOME, DEFAULT_EMAIL
from string import Template
from django_tables2 import RequestConfig
from tables import UsersTable, GroupsTable

def index(request):
    return render_to_response(
        'index.html',
        context_instance=RequestContext(request)
    )

def users(request):
    context = {}
    table = UsersTable(LdapUser.objects.all())
    RequestConfig(request).configure(table)
    context = {
        'table': table,
    }
    return render_to_response(
        'users.html',
        context,
        context_instance=RequestContext(request)
    )

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
    return render_to_response(
        'user.html',
        context,
        context_instance=RequestContext(request)
    )

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

def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if not form.is_valid():
            print form.errors
        if form.is_valid():
            user = form.save(commit=False)
            groups = form.cleaned_data.get('groups')
            update_groups_membership(user, groups)
            user.save()
            return redirect('user', user.uid)
    context = {
        'form': form,
    }
    return render_to_response(
        'user.html',
        context,
        context_instance=RequestContext(request)
    )

def groups(request):
    context = {}
    table = GroupsTable(LdapGroup.objects.all())
    RequestConfig(request).configure(table)
    context = {
        'table': table,
    }
    return render_to_response(
        'groups.html',
        context,
        context_instance=RequestContext(request)
    )

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
    return render_to_response(
        'group.html',
        context,
        context_instance=RequestContext(request)
    )

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
    return render_to_response(
        'group.html',
        context,
        context_instance=RequestContext(request)
    )

def sudoers(request):
    pass

def settings(request):
    form = SettingsForm()
    context = {
        'form': form,
    }
    return render_to_response(
        'settings.html',
        context,
        context_instance=RequestContext(request)
    )

def make_home_path(user):
    return DEFAULT_HOME.safe_substitute(username=user.username)

def make_email_adress(user):
    return DEFAULT_EMAIL.safe_substitute(username=user.username)
