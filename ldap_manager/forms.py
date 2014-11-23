from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField
from models import LdapUser, LdapGroup

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

    auto_uid = BooleanField(
        initial=True,
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
        dn needs to be blank in order to save new object
        '''
        exclude = ['group', 'dn']
        #exclude = ['dn']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # support bootstrap
        for f in UserForm.base_fields.values():
            f.widget.attrs['class'] = 'form-control'
