from decore_base import decore
from decore_base.classes.decore_base import Decore_base as Base
from models.company_model import Company_model as Model

@decore.base(p_title='Companies', p_model=Model)
class Company_base(Base):
    
    @decore.widget(p_parent_id='per_vi1_di1_wi1', p_title='Companies', p_type='table', p_active_s=Model.field_s)
    def per_vi1_di1_wi1_wi2():
        pass

    @decore.view(p_parent_id='Global_management_base', p_title='Companies', p_icon='mdi-domain', p_active_s=Model.field_s)
    def com_vi1():
        @decore.dialog(p_title='Company', p_type='standard', p_display='drawer', p_activator='item-click')
        def com_vi1_di1():
            pass