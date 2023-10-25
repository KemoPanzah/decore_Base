from ..decore import decore
from ..models.bi_account_model import BI_Account_model as Model

@decore.base(title='Account', model=Model)
class BI_Account_base:
    @decore.function(type='shot')
    def bi_acc_fu1(self):
        if Model.get_or_none(Model.username == 'guest@decore.base') is None:
            guest = Model()
            guest.title = 'Guest Account'
            guest.desc = 'Account to log in automatically as user with guest role'
            guest.username = 'guest@decore.base'
            guest.password = decore.mayor.hash_password('password')
            guest.save()
        
        if Model.get_or_none(Model.username == 'admin@decore.base') is None:
            admin = Model()
            admin.title = 'Admin Account'
            admin.desc = 'Account to log in as user with admin role'
            admin.username = 'admin@decore.base'
            admin.password = decore.mayor.hash_password('password')
            admin.role = 10
            admin.save()

    @decore.view(title='Accounts', type='table', fields=Model.field_s)
    def bi_accounts_view():
        pass
    @decore.view(title='Login', type='empty')
    def bi_login_view():
        @decore.dialog(title='Login', type='standard', activator='empty')
        def bi_login_dialog():
            @decore.widget(title='Login', type='form', fields=[Model.username, Model.password])
            def bi_login_form():
                @decore.action(title='Login', icon='mdi-login' , type='login', activator='default')
                def bi_login_action(self, item, **kwargs):
                    t_token = decore.mayor.login(item.username, item.password)
                    if t_token:
                        return True, 'Loging in ' + item.username, t_token
                    else:
                        return False, 'Wrong username or password'
                