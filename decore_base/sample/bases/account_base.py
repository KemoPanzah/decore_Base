from decore_base import decore
from models.account_model import Account_model as Model

@decore.base(title='Accounts', model=Model)
class Account_base:
    @decore.widget(parent_id='per_vi1_di1_wi1', title='Accounts' , type='table', fields=[Model.title, Model.email])
    def per_vi1_di1_wi1_wi1():
        pass

    @decore.view(parent_id='Information_system_base', title='Accounts',icon='mdi-account-circle-outline', type='table', fields=Model.field_s, filters=[Model.password ,Model.person])
    def acc_vi1():
        pass