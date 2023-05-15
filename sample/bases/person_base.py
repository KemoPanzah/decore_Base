from decore_base import decore
from decore_base.classes.decore_base import Decore_base as Base
from models.person_model import Person_model as Model

@decore.base(p_title='Person', p_model=Model)
class Person_base(Base):
    @decore.view(p_parent_id='Global_management_base', p_title='Persons', p_icon='mdi-account-group-outline', p_type='table', p_active_s=Model.field_s, p_filter_s=[Model.academic_degree, Model.br_companies, Model.br_accounts])
    def per_vi1():
        @decore.dialog(p_title='Person', p_type='standard', p_display='drawer', p_activator='item-click')
        def per_vi1_di1():
            @decore.widget(p_title='Informations', p_type='info', p_active_s=Model.field_s)
            def per_vi1_di1_wi1():
                @decore.dialog(p_title='Edit Person', p_icon='mdi-pencil', p_type='standard', p_display='drawer', p_activator='item-menu')
                def per_vi1_wi1_di1():
                    @decore.widget(p_type='form', p_active_s=[Model.last_name])
                    def per_vi1_di1_wi1_di1_wi1():
                        @decore.action(p_activator='item-submit')
                        def per_vie_di1_wi1_di1_wi1_ac1(self, p_data):
                            return True, 'Hier ist alles Super!'