from ..decore import decore
from ..classes.decore_mayor import Decore_mayor as Mayor

@decore.base(title='Mayor', model=Mayor)
class dbi_mayor:
    @decore.function(type='shot')
    def bi_acc_fu1(self):
        if Mayor.get_or_none(Mayor.username == 'guest@decore.base') is None:
            guest = Mayor()
            guest.title = 'Guest Account'
            guest.desc = 'Account to log in automatically as user with guest role'
            guest.username = 'guest@decore.base'
            guest.password = Mayor.hash_password('password')
            guest.save()
        
        if Mayor.get_or_none(Mayor.username == 'admin@decore.base') is None:
            admin = Mayor()
            admin.title = 'Admin Account'
            admin.desc = 'Account to log in as user with admin role'
            admin.username = 'admin@decore.base'
            admin.password = Mayor.hash_password('password')
            admin.role = 10
            admin.save()

    @decore.view(title='Accounts', type='table', fields=Mayor.field_s)
    def bi_accounts_view():
        pass
    @decore.view(title='Login', type='empty')
    def bi_login_view():
        @decore.dialog(title='Login', type='standard', activator='empty')
        def bi_login_dialog():
            @decore.widget(title='Login', type='form', fields=[Mayor.username, Mayor.password])
            def bi_login_form():
                @decore.action(title='Login', icon='mdi-login' , type='login', activator='default')
                def bi_login_action(self, item, **kwargs):
                    t_token = Mayor.login(item.username, item.password)
                    if t_token:
                        return True, 'Loging in ' + item.username, t_token
                    else:
                        return False, 'Wrong username or password'
                
