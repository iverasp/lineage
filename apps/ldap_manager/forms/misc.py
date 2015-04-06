from django.forms import ModelForm, ModelChoiceField, \
    ModelMultipleChoiceField, BooleanField, ChoiceField, Form, CharField, \
    PasswordInput, IntegerField
from apps.ldap_manager.models import LdapUser, LdapGroup
from lineage.settings import SHELLS, DEFAULT_HOME, DEFAULT_EMAIL, \
    MIN_UID, MIN_GID
from django.core.exceptions import ValidationError
from django_password_strength.widgets import PasswordStrengthInput, \
    PasswordConfirmationInput


class SettingsForm(Form):
    pass
