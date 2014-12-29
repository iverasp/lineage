import django_tables2 as tables
from models import LdapUser, LdapGroup

class BaseTable(tables.Table):

    edit = tables.LinkColumn(
        'user',
        verbose_name='Edit',
        sortable=False,
        empty_values=(),
        args=[tables.A('pk')]
    )

    selected = tables.CheckBoxColumn(
        verbose_name='Select',
        accessor='pk',
        sortable=False,
        visible=False
    )

    tr_class = tables.Column(
        visible=False,
        empty_values=(),
        accessor='pk',
        )

    username = tables.Column(
        visible=False,
        empty_values=(),
        accessor='pk',
        )

    def render_edit(self):
        return 'Edit'

    def render_tr_class(self, value):
        return 'table_row'

class UsersTable(BaseTable):

    headline = 'Users'
    baseurl = 'user'

    class Meta:
        model = LdapUser
        fields = ('full_name', 'username', 'uid')
        empty_text = 'No users found'
        order_by = ('full_name')
        template = 'table.html'

class GroupsTable(BaseTable):

    headline = 'Groups'
    baseurl = 'group'

    class Meta:
        model = LdapGroup
        fields = ('name', 'gid')
        empty_text = 'No groups found'
        order_by = ('name')
        template = 'table.html'
