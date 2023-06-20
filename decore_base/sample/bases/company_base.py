from decore_base import decore
from models.company_model import Company_model as Model

@decore.base(title='Companies', model=Model)
class Company_base:
    
    @decore.widget(parent_id='per_vi1_di1_wi1', title='Companies', type='table', fields=Model.field_s)
    def per_vi1_di1_wi1_wi2():
        pass

    @decore.view(parent_id='Global_management_base', title='Companies', icon='mdi-domain', fields=Model.field_s)
    def com_vi1():
        @decore.dialog(title='Company', type='standard', display='drawer', activator='item-click')
        def com_vi1_di1():
            pass