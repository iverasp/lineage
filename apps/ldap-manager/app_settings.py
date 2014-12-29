from string import Template

BASE_DN="dc=iegget,dc=no"

SHELLS = (
    ('/bin/false', 'false'),
    ('/bin/bash', 'bash'),
    ('/bin/zsh', 'zsh'),
)

DEFAULT_HOME = Template('/home/$username')
DEFAULT_EMAIL = Template('$username@stud.ntnu.no')
