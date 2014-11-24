from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField, ChoiceField, Form, CharField, \
    PasswordInput, IntegerField
from models import LdapUser, LdapGroup
from settings import SHELLS
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

    enable_samba = BooleanField(
        required=False
    ) # TODO: find users samba settings here

    class Meta:
        model = LdapUser
        fields = '__all__'
        '''
        group is defined above
        uid needs to be evaluated if set to auto
        dn needs to be blank in order to save new object
        '''
        #exclude = ['group', 'dn']
        exclude = ['dn']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # support bootstrap
        for f in UserForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        # cn should be givenName + sn
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
        else: # means we want to change UID of user
            # check if entered UID is in use and is not our own
            user = LdapUser.objects.filter(uid=cleaned_data.get('uid')).first()
            if user and not user == self.instance:
                raise ValidationError('%s is already in use' % cleaned_data.get('uid'))

        # somehow UID is still not set... do we need this?
        if not cleaned_data.get('uid'):
            cleaned_data['uid'] = unicode(self.instance.uid)

        # if UID changes we need to remove current UID from all groups
        if not cleaned_data.get('uid') == unicode(self.instance.uid):
            self.update_groups_membership(self.instance, [])

        return cleaned_data

    def find_next_uid(self):
        # execute external script to find next UID
        return unicode(2035)

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

class UpdatePasswordForm(Form):

    password = CharField(
        label="New password",
        max_length=100,
        widget=PasswordInput
    )
