
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
