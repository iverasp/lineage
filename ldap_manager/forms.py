from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField
from models import LdapUser, LdapGroup

class UserForm(ModelForm):
    group = ModelChoiceField(
        queryset=LdapGroup.objects.all(),
        to_field_name='gid'
    )

    groups = ModelMultipleChoiceField(
        queryset=LdapGroup.objects.all(),
        to_field_name='gid',
        required=False
    )

    auto_uid = BooleanField(
        initial=True,
        required=False
    ) # TODO: this setting is not stored anywhere. how to solve?

    enable_samba = BooleanField(
        initial=True,
        required=False
    ) # TODO: find users samba settings here

    class Meta:
        model = LdapUser
        fields = '__all__'
        # group is defined above
        exclude = ['group']
        '''
        fields = [
            'uid',
            'group',
            'username',
            'first_name',
            'last_name',
            'email'
            ]
        '''


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # support bootstrap
        for f in UserForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'
