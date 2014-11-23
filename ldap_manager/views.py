from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from ldap_manager.models import LdapGroup, LdapUser
from forms import *

def index(request):
    t = loader.get_template('index.html')
    c = Context()
    return HttpResponse(t.render(c))

def users(request):
    context = {}
    context['lol'] = 'cats'
    users = LdapUser.objects.all()
    groups = LdapGroup.objects.all()
    for group in groups:
        print group.usernames
    t = loader.get_template('users.html')
    c = Context({'user_list': users, 'group_list': groups})
    return HttpResponse(t.render(c))

def user(request, uid):
    user = LdapUser.objects.filter(uid=uid).first()
    if not user:
        pass
    form = UserForm(
        instance=user,
        initial= {
            'group': LdapGroup.objects.filter(
                gid=unicode(user.group)
            ).first(),
            'groups':LdapGroup.objects.filter(
                usernames__contains=unicode(user.group)
            ).all()
        }
    )
    if request.method == 'POST':
        form = UserForm(data=request.POST, instance=user)
        if form.is_valid():
            print "valid!"
            # logic for groups membership
            groups = form.cleaned_data.get('groups')
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

def update_groups_membership(user, groups):
    old_groups = LdapGroup.objects.filter(
        usernames__contains=unicode(user.uid)
    ).all()
    new_groups = groups
    pos_diff = list(set(new_groups) - set(old_groups))
    neg_diff = list(set(old_groups) - set(new_groups))
    for group in pos_diff:
        ldap_group = LdapGroup.objects.filter(
            gid=group.gid
        ).first()
        ldap_group.usernames.append(unicode(user.uid))
        ldap_group.save()
    for group in neg_diff:
        ldap_group = LdapGroup.objects.filter(
            gid=group.gid
        ).first()
        ldap_group.usernames.remove(unicode(user.uid))
        ldap_group.save()

def groups(request):
    pass

def group(request):
    pass

def sudoers(request):
    pass
