from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from ldap_manager.models import LdapGroup, LdapUser
from forms import *
from settings import DEFAULT_HOME
from string import Template

def index(request):
    return render_to_response(
        'index.html',
        context_instance=RequestContext(request)
    )

def users(request):
    context = {}
    users = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    context = {
        'user_list': users,
        'group_list': groups
    }
    return render_to_response(
        'users.html',
        context,
        context_instance=RequestContext(request)
    )

def user(request, uid):
    user = LdapUser.objects.filter(uid=uid).first()
    if not user:
        return redirect('users')
    #print user.password
    form = UserForm(
        instance=user,
        initial= {
            'group': LdapGroup.objects.filter(
                gid=unicode(user.group)
            ).first(),
            'groups': LdapGroup.objects.filter(
                usernames__contains=unicode(user.uid)
            ).all(),
            'enable_samba': False,
            'auto_uid': True,
            'auto_home': True,
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
            return redirect('user', user.uid)
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
    users = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    context = {
        'user_list': users,
        'group_list': groups
    }
    return render_to_response(
        'groups.html',
        context,
        context_instance=RequestContext(request)
    )

def group(request, gid):
    group = LdapGroup.objects.filter(gid=gid).first()
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
