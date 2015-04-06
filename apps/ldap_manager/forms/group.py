from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField, ChoiceField, Form, CharField, \
    PasswordInput, IntegerField
from apps.ldap_manager.models import LdapUser, LdapGroup
from lineage.settings import SHELLS, DEFAULT_HOME, DEFAULT_EMAIL, \
    MIN_UID, MIN_GID
from django.core.exceptions import ValidationError
from django_password_strength.widgets import PasswordStrengthInput, \
    PasswordConfirmationInput

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

    def clean(self):
        cleaned_data = super(GroupForm, self).clean()

        # GID related stuff goes here
        if cleaned_data.get('auto_gid'):
            # if we have a GID it does not need changing
            if self.instance.gid > 0:
                cleaned_data['gid'] = unicode(self.instance.gid)
            # if we don't have a UID it means we're a new user
            else:
                cleaned_data['gid'] = self.find_next_gid()

        return cleaned_data

    def find_next_gid(self):
        # TODO: see find_next_uid() above
        if LdapGroup.objects.exists():
            next_gid = LdapGroup.objects.latest('gid').gid + 1
            if next_gid > MIN_GID: return next_gid
        return MIN_GID
