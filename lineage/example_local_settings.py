
DEBUG = True
TEMPLATE_DEBUG = DEBUG

#Overide this here!
SECRET_KEY = 'some_random_secret_key'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'ldapdb.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    },
    'ldap': {
        'ENGINE': 'ldapdb.backends.ldap',
        'NAME': 'ldap://example.com',
        'USER': 'cn=admin,dc=example,dc=com',
        'PASSWORD': 'secretpassword',
        #'TLS': True,
        #'CONNECTION_OPTIONS': {
        #    ldap.OPT_X_TLS_DEMAND: True,
        #}
    }
}

BASE_DN="dc=herpderp,dc=no"

MIN_UID = 2000
MIN_GID = 2000

ADDITIONAL_SHELLS= (

    # Add additional shells with syntax
    # ('/path/to/shell', 'name'),

    ('/bin/zsh', 'zsh'),
)

from string import Template
DEFAULT_HOME = Template('/home/$username')
DEFAULT_EMAIL = Template('$username@stud.ntnu.no')
