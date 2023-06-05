from decore_base import decore
from decore_base.classes.decore_base import Decore_base as Base
from models.person_model import Person_model as Model

@decore.base(p_title='Person', p_model=Model)
class Person_base(Base):
    
    @decore.widget(p_parent_id='com_vi1_di1', p_title='Persons', p_type='table', p_active_s=Model.field_s)
    def com_vi1_di1_wi1():
        pass

    @decore.view(p_parent_id='Global_management_base', p_title='Persons', p_icon='mdi-account-group-outline', p_type='table', p_active_s=Model.field_s, p_filter_s=[Model.academic_degree, Model.companies, Model.accounts])
    def per_vi1():
        
        @decore.dialog(p_title='Add person...', p_icon='mdi-plus' , p_type='standard', p_activator='default-menu')
        def per_vi1_di3():
            @decore.widget(p_type='form', p_active_s=[Model.first_name, Model.last_name, Model.academic_degree, Model.age, Model.capacity])
            def per_vi1_di3_wi1():
                @decore.action(p_type='submit')
                def per_vi1_di3_wi1_ac1(self, p_data):
                    return True, 'Success!'
        
        @decore.action(p_title='Test action', p_icon='mdi-test-tube', p_type='standard', p_activator='default-menu')
        def per_vi1_ac1(self, p_data):
            pass

        @decore.dialog(p_title='Person', p_type='standard', p_display='drawer', p_activator='item-click')
        def per_vi1_di1():
            @decore.widget(p_title='Informations', p_type='info', p_active_s=Model.field_s)
            def per_vi1_di1_wi1():
                @decore.dialog(p_title='Edit Person', p_icon='mdi-pencil', p_type='standard', p_display='drawer', p_activator='item-menu')
                def per_vi1_wi1_di1():
                    @decore.widget(p_type='form', p_active_s=[Model.first_name, Model.last_name])
                    def per_vi1_di1_wi1_di1_wi1():
                        @decore.action(p_type='submit')
                        def per_vi1_di1_wi1_di1_wi1_ac1(self, p_data):
                            return True, 'Success!'
        
        @decore.dialog(p_title='Edit Person', p_icon='mdi-pencil', p_type='standard', p_display='drawer', p_activator='item-menu')
        def per_vi1_di2():
            @decore.widget(p_type='form', p_active_s=[Model.first_name, Model.last_name])
            def per_vi1_di2_wi1():
                @decore.action(p_type='submit')
                def per_vi1_di2_wi1_ac1(self, p_data):
                    return True, 'Success!'