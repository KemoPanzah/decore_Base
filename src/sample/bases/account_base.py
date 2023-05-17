from decore_base import decore
from decore_base.classes.decore_base import Decore_base as Base
from models.account_model import Account_model as Model

@decore.base(p_title='Accounts', p_model=Model)
class Account_base(Base):
    @decore.widget(p_parent_id='per_vi1_di1_wi1', p_title='Accounts' , p_type='table', p_active_s=[Model.title, Model.email])
    def per_vi1_di1_wi1_wi1():
        pass

    @decore.view(p_parent_id='Information_system_base', p_title='Accounts',p_icon='mdi-account-circle-outline', p_type='table', p_active_s=Model.field_s, p_filter_s=[Model.password ,Model.person])
    def acc_vi1():
        pass