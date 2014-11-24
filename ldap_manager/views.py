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
            # logic for groups membership
            groups = form.cleaned_data.get('groups')
            update_groups_membership(user, groups)
            # hack? probably better to use ModelChoiceField correctly
            #user.group = form.cleaned_data.get('group').gid
            enable_samba = form.cleaned_data.get('enable_samba')
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
    pass

def group(request):
    pass

def sudoers(request):
    pass

def update_groups_membership(user, new_groups):
    old_groups = LdapGroup.objects.filter(
        usernames__contains=unicode(user.uid)
    ).all()
    pos_diff = list(set(new_groups) - set(old_groups))
    neg_diff = list(set(old_groups) - set(new_groups))
    for group in pos_diff:
        group = LdapGroup.objects.filter(
            gid=group.gid
        ).first()
        group.usernames.append(unicode(user.uid))
        print "added to group", group
        group.save()
    for group in neg_diff:
        group = LdapGroup.objects.filter(
            gid=group.gid
        ).first()
        group.usernames.remove(unicode(user.uid))
        print "removed from group", group
        group.save()

def make_home_path(user):
    print DEFAULT_HOME.safe_substitute(username=user.username)
