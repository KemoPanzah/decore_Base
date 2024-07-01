from ..decore import decore
from ..classes.decore_mayor import Decore_mayor as Mayor

@decore.base(title='Mayor', icon='mdi-security' ,model=Mayor, role=10)
class dbi_mayor:
    @decore.function(type='shot')
    def dbi_mayor_init(self):
        if Mayor.get_or_none(Mayor.username == 'guest@decore.base') is None:
            guest = Mayor()
            guest.owner_id = guest.id
            guest.title = 'Guest Account'
            guest.desc = 'Account to log in automatically as user with guest role'
            guest.username = 'guest@decore.base'
            guest.password = Mayor.hash_password('password')
            guest.save()
        
        if Mayor.get_or_none(Mayor.username == 'admin@decore.base') is None:
            admin = Mayor()
            admin.owner_id = admin.id
            admin.title = 'Admin Account'
            admin.desc = 'Account to log in as user with admin role'
            admin.username = 'admin@decore.base'
            admin.password = Mayor.hash_password('password')
            admin.role = 10
            admin.save()

    @decore.view(title='Accounts', type='table', fields=Mayor.field_s)
    def dbi_accounts_view():
        pass
    
@decore.base(title='Mayor private', model=Mayor, private=True, stretch=True, hide=True, role=0)
class dbi_mayor_priv:
    @decore.dialog(parent_id='app', icon='mdi-account-settings' ,activator='last', role=2)
    def dbi_account_dialog():
        @decore.widget(title='Account Info', type='info', fields=[Mayor.title, Mayor.username, Mayor.desc, Mayor.role])
        def dbi_account_info():
            @decore.action(title='Logout', icon='mdi-logout' , type='standard', activator='default')
            def dbi_logout_action(self, item, token, **kwargs):
                token['value'] = 'remove'
                return True, 'Loging out ' + item.username

    @decore.view(title='Login', type='empty', role=0)
    def dbi_login_view():
        @decore.dialog(title='Login', type='standard', activator='empty', role=0)
        def dbi_login_dialog():
            @decore.widget(title='Login', type='form', fields=[Mayor.username, Mayor.password], role=0)
            def dbi_login_form():
                @decore.action(title='Login', icon='mdi-login', type='submit', errors=False, role=0)
                def dbi_login_action(self, item, token, **kwargs):
                    t_account = Mayor.get_account_from_identity(item.username)
                    if t_account:
                        t_account.set_token(item.password)
                        if t_account.token:
                            token['value'] = t_account.token
                            return True, 'Loging in ' + t_account.username
                        else:
                            return False, 'Wrong password'
                    else:
                        return False, 'Wrong username'
        