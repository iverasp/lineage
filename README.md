# About

Lineage is a LDAP web frontend written in Python and Django using [django-ldapdb](https://github.com/jlaine/django-ldapdb).

This software is at the moment in early development and has some bugs.

## Features
Working features are:

  - User and group overview
  - Add user
  - Add group
  - Edit user
  - Edit group
  - Basic ldap auth (only django login)

Planned features:

  - Proper login page for admins
  - User creation wizard for events
  - Change password wizard

# Installation

### OS dependencies
  apt-get build-dep python-ldap
