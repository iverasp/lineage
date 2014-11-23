from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from ldap_manager.models import LdapGroup, LdapUser
from forms import *

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
        # redirect or something...
        pass
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
        }
    )
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=user)
        if not form.is_valid():
            print form.data
            print form.errors
        if form.is_valid():
            print "valid!"
            # logic for groups membership
            groups = form.cleaned_data.get('groups')
            # hack? probably better to use ModelChoiceField correctly
            user.group = form.cleaned_data.get('group').gid
            update_groups_membership(user, groups)
            enable_samba = form.cleaned_data.get('enable_samba')
            auto_uid = form.cleaned_data.get('auto_uid')
            form.save()
    context = {
        'user': user,
        'form': form,
    }
    return render_to_response(
        'user.html',
        context,
        context_instance=RequestContext(request)
    )

def add_user(request):
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(data=request.POST)
        if not form.is_valid():
            print form.errors
        if form.is_valid():
            form.save(commit=True)
            print form

    context = {
        'form': form,
    }
    return render_to_response(
        'user.html',
        context,
        context_instance=RequestContext(request)
    )

def update_groups_membership(user, groups):
    old_groups = LdapGroup.objects.filter(
        usernames__contains=unicode(user.uid)
    ).all()
    new_groups = groups
    pos_diff = list(set(new_groups) - set(old_groups))
    neg_diff = list(set(old_groups) - set(new_groups))
    print "pos diff", pos_diff
    print "neg diff", neg_diff
    for group in pos_diff:
        ldap_group = LdapGroup.objects.filter(
            gid=group.gid
        ).first()
        ldap_group.usernames.append(unicode(user.uid))
        print "added to group", ldap_group
        ldap_group.save()
    for group in neg_diff:
        ldap_group = LdapGroup.objects.filter(
            gid=group.gid
        ).first()
        ldap_group.usernames.remove(unicode(user.uid))
        print "removed from group", ldap_group
        ldap_group.save()

def groups(request):
    pass

def group(request):
    pass

def sudoers(request):
    pass
