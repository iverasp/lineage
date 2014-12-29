from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField, ChoiceField, Form, CharField, \
    PasswordInput, IntegerField
from models import LdapUser, LdapGroup
from django_ldap_manager.settings import SHELLS, DEFAULT_HOME, DEFAULT_EMAIL
from django.core.exceptions import ValidationError
from django_password_strength.widgets import PasswordStrengthInput, PasswordConfirmationInput

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
    )
    # TODO: this setting is not stored anywhere. how to solve?
    # Maybe it should always be on? Only in rare cases
    # would a user need to specify their UID.

    auto_home = BooleanField(
        required=False
    )
    # TODO: this setting is not stored anywhere. how to solve?
    # Currently fixed by checking if the path is the same as the one
    # that would be generated automatically (see views.py)

    auto_email = BooleanField(
        required=False
    )
    # TODO: this setting is not stored anywhere. how to solve?
    # Currently fixed by checking if the email is the same as the one
    # that would be generated automatically (see views.py)

    enable_samba = BooleanField(
        required=False
    ) # TODO: find users samba settings here

    class Meta:
        model = LdapUser
        fields = '__all__'
        exclude = ['dn', 'password']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # support bootstrap
        for f in UserForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        # cn should be givenName + sn
        # the if below should already have been taken care of by model...
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
            print 'got uid?'
            # if we have a UID it does not need changing
            if self.instance.uid > 0:
                cleaned_data['uid'] = unicode(self.instance.uid)
            # if we don't have a UID it means we're a new user
            else:
                cleaned_data['uid'] = self.find_next_uid()

        # if UID changes we need to remove current UID from all groups
        if not cleaned_data.get('username') == unicode(self.instance.username):
            self.update_groups_membership(self.instance, [])

        # home directory stuff goes here
        if cleaned_data.get('auto_home'):
            cleaned_data['home_directory'] = self.make_home_path(cleaned_data)

        # email stuff goes here
        if cleaned_data.get('auto_email'):
            cleaned_data['email'] = self.make_email_adress(self.instance)

        # did we change the primary key? that was stupid...
        if not cleaned_data.get('username') == unicode(self.instance.username):
            user = LdapUser.objects.filter(username=self.instance.username).first()
            user.username = cleaned_data.get('username')
            user.save()
            self.instance = user

        # update group memeberships
        self.update_groups_membership(self.instance, cleaned_data.get('groups'))

        # photo is returned as unicode and causes TypeError
        cleaned_data['photo'] = str(cleaned_data['photo'])

        return cleaned_data

    def find_next_uid(self):
        # TODO: execute external script to find next UID
        return unicode(4333)

    def update_groups_membership(self, user, new_groups):
        old_groups = LdapGroup.objects.filter(
            usernames__contains=unicode(user.username)
        ).all()
        pos_diff = list(set(new_groups) - set(old_groups))
        neg_diff = list(set(old_groups) - set(new_groups))
        for group in pos_diff:
            group = LdapGroup.objects.filter(
                gid=group.gid
            ).first()
            group.usernames.append(unicode(user.username))
            print "added", user.username, "to group", group
            group.save()
        for group in neg_diff:
            group = LdapGroup.objects.filter(
                gid=group.gid
            ).first()
            group.usernames.remove(unicode(user.username))
            print "removed", user.username, "from group", group
            group.save()

    def make_home_path(self, data):
        return DEFAULT_HOME.safe_substitute(username=data.get('username'))

    def make_email_adress(self, user):
        return DEFAULT_EMAIL.safe_substitute(username=user.username)

class UpdatePasswordForm(Form):

    password = CharField(
        label="New password",
        max_length=100,
        widget=PasswordStrengthInput()
    )

    confirm_password = CharField(
        widget=PasswordConfirmationInput(confirm_with='password')
    )

    def __init__(self, *args, **kwargs):
        super(UpdatePasswordForm, self).__init__(*args, **kwargs)
        # support bootstrap
        for f in UpdatePasswordForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'

class GroupForm(ModelForm):

    usernames = ModelMultipleChoiceField(
        queryset = LdapUser.objects.none(),
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
        obj = kwargs.get('instance', None)
        gid = None
        if obj: gid = obj.gid
        super(GroupForm, self).__init__(*args, **kwargs)

        if gid: # dont know what to do here yet...
            self.fields['usernames'].queryset = LdapUser.objects.filter(
                username__in=LdapGroup.objects.filter(
                    gid=unicode(gid)
                ).first().usernames
            ).all()

        # support bootstrap
        for f in GroupForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'

    def find_next_gid(self):
        # TODO: execute external script to find next GID
        return unicode(4002)

class SettingsForm(Form):
    pass
