from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField, ChoiceField, Form, CharField, \
    PasswordInput, IntegerField
from models import LdapUser, LdapGroup
from settings import SHELLS, DEFAULT_HOME
from django.core.exceptions import ValidationError

class UserForm(ModelForm):

    group = ModelChoiceField(
        queryset=LdapGroup.objects.all(),
        to_field_name='gid',
        empty_label=None
    )

    groups = ModelMultipleChoiceField(
        queryset=LdapGroup.objects.all(),
        to_field_name='gid',
        required=False
    )

    login_shell = ChoiceField(
        choices=SHELLS
    )

    uid = IntegerField(
        required=False,
        min_value=1000,
    )

    auto_uid = BooleanField(
        required=False
    ) # TODO: this setting is not stored anywhere. how to solve?

    auto_home = BooleanField(
        required=False
    ) # TODO: this setting is not stored anywhere. how to solve?

    enable_samba = BooleanField(
        required=False
    ) # TODO: find users samba settings here

    class Meta:
        model = LdapUser
        fields = '__all__'
        exclude = ['dn']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # support bootstrap
        for f in UserForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        # cn should be givenName + sn
        # this should already have been taken care of by model
        if cleaned_data.get('first_name') and cleaned_data.get('last_name'):
            cleaned_data['full_name'] = cleaned_data.get('first_name') + \
                ' ' + cleaned_data.get('last_name')
        else:
            raise ValidationError('You must supply first and last names')
        # this could be fixed in ModelChoiceField?
        if cleaned_data.get('group'):
            cleaned_data['group'] = cleaned_data.get('group').gid
        # UID related stuff goes here
        if cleaned_data.get('auto_uid'):
            # if we have a UID it does not need changing
            if self.instance.uid > 0:
                cleaned_data['uid'] = unicode(self.instance.uid)
            # if we don't have a UID it means we're a new user
            else:
                cleaned_data['uid'] = self.find_next_uid()

        # if UID changes we need to remove current UID from all groups
        if not cleaned_data.get('uid') == unicode(self.instance.uid):
            self.update_groups_membership(self.instance, [])
        self.update_groups_membership(self.instance, cleaned_data.get('groups'))

        # home directory stuff goes here
        if cleaned_data.get('auto_home'):
            cleaned_data['home_directory'] = self.make_home_path(cleaned_data)

        return cleaned_data

    def find_next_uid(self):
        # TODO: execute external script to find next UID
        return unicode(2043)

    def update_groups_membership(self, user, new_groups):
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

    def make_home_path(self, data):
        return DEFAULT_HOME.safe_substitute(username=data.get('username'))

class UpdatePasswordForm(Form):

    password = CharField(
        label="New password",
        max_length=100,
        widget=PasswordInput
    )

class GroupForm(ModelForm):

    usernames = ModelMultipleChoiceField(
        queryset = LdapUser.objects.all(),
        to_field_name='uid',
        required=False
    )

    auto_gid = BooleanField(
        required=False
    ) # TODO: this setting is not stored anywhere. how to solve?

    class Meta:
        model = LdapGroup
        fields = '__all__'
        exclude = ['dn']

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        gid = kwargs.pop('gid', None)
        if gid: # dont know what to do here yet...
            self.fields['usernames'].queryset = LdapUser.objects.filter(
                uid__in=LdapGroup.objects.filter(
                    gid=unicode(gid)
                ).first().usernames
            ).all()
        else:
            self.fields['usernames'].queryset = LdapUser.objects.none()

        # support bootstrap
        for f in GroupForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'
