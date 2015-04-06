from lineage.settings import DEFAULT_HOME, DEFAULT_EMAIL

def make_home_path(user):
    return DEFAULT_HOME.safe_substitute(username=user.username)

def make_email_adress(user):
    return DEFAULT_EMAIL.safe_substitute(username=user.username)
