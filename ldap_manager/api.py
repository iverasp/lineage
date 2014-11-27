from tastypie.resources import ModelResource, Resource
from models import LdapUser, LdapGroup
from django.db.models import Q

class UserResource(ModelResource):
    class Meta:
        queryset = LdapUser.objects.all()
        resource_name = 'user'
        fields = ['username', 'uid']

class GroupResource(ModelResource):
    class Meta:
        queryset = LdapGroup.objects.all()
        resource_name = 'group'
        fields = ['name', 'gid', 'usernames']

class AjaxSearchResource(Resource):
    class Meta:
        resource_name = 'ajaxsearch'
        allowed_methods = ['post']

    def post_list(self, request, **kwargs):
        phrase = request.POST.get('q')
        if phrase:
            print LdapUser.objects.filter(username__contains='adaas').all()
            users = list(LdapUser.objects.filter(
                Q(username__contains=phrase) |
                Q(full_name__contains=phrase)
            ).values(
                'username',
                'full_name'
            ))
            return self.create_response(request, {'users': users})
