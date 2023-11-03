from ..decore import decore
from ..classes.decore_mayor import Decore_mayor as Mayor

@decore.base(title='Mayor', model=Mayor)
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
    
@decore.base(title='Mayor private', model=Mayor, private=True)
class dbi_mayor_priv:
    @decore.dialog(parent_id='app', icon='mdi-account' ,activator='last', role=1)
    def dbi_account_dialog():
        @decore.widget(title='Account Info', type='info', fields=[Mayor.title, Mayor.username, Mayor.desc, Mayor.role])
        def dbi_account_info():
            @decore.action(title='Logout', icon='mdi-logout' , type='login', activator='default')
            def dbi_logout_action(self, item, **kwargs):
                return True, 'Loging out ' + item.username, None

    @decore.view(title='Login', type='empty')
    def bi_login_view():
        @decore.dialog(title='Login', type='standard', display="draw-half", activator='empty')
        def dbi_login_dialog():
            @decore.widget(title='Login', type='form', fields=[Mayor.username, Mayor.password])
            def dbi_login_form():
                @decore.action(title='Login', icon='mdi-login' , type='login', activator='default')
                def dbi_login_action(self, item, **kwargs):
                    t_token = Mayor.get_token(item.username, item.password)
                    if t_token:
                        return True, 'Loging in ' + item.username, t_token
                    else:
                        return False, 'Wrong username or password'
        