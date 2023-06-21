from decore_base import decore
from models.person_model import Person_model as Model

@decore.base(title='Person', model=Model)
class Person_base:
    @decore.widget(parent_id='com_vi1_di1', title='Persons', type='table', fields=Model.field_s)
    def com_vi1_di1_wi1():
        pass
    @decore.view(parent_id='Global_management_base', title='Persons', icon='mdi-account-group-outline', type='table', fields=Model.field_s, filters=[Model.academic_degree, Model.companies, Model.accounts])
    def per_vi1():
        @decore.dialog(title='Add person...', icon='mdi-plus' , type='standard', activator='default-menu')
        def per_vi1_di3():
            @decore.widget(type='form', fields=[Model.first_name, Model.last_name, Model.academic_degree, Model.age, Model.capacity])
            def per_vi1_di3_wi1():
                @decore.action(type='submit')
                def per_vi1_di3_wi1_ac1(self, p_data):
                    t_item = Model(p_data['item'])
                    t_item.title = t_item.first_name + ' ' + t_item.last_name
                    if t_item.save():
                        return True, 'Success!'
                    else:
                        return False, 'Error!'
        @decore.action(title='Test action', icon='mdi-test-tube', type='standard', activator='default-menu')
        def per_vi1_ac1(self, p_data):
            return True, 'Success!'
        @decore.dialog(title='Person', type='standard', display='drawer', activator='item-click')
        def per_vi1_di1():
            @decore.widget(title='Informations', type='info', fields=Model.field_s)
            def per_vi1_di1_wi1():
                @decore.dialog(title='Edit Person', icon='mdi-pencil', type='standard', display='drawer', activator='item-menu')
                def per_vi1_wi1_di1():
                    @decore.widget(type='form', fields=[Model.first_name, Model.last_name])
                    def per_vi1_di1_wi1_di1_wi1():
                        @decore.action(type='submit')
                        def per_vi1_di1_wi1_di1_wi1_ac1(self, p_data):
                            return True, 'Success!'
        @decore.dialog(title='Edit Person', icon='mdi-pencil', type='standard', display='drawer', activator='item-menu')
        def per_vi1_di2():
            @decore.widget(type='form', fields=[Model.first_name, Model.last_name])
            def per_vi1_di2_wi1():
                @decore.action(type='submit')
                def per_vi1_di2_wi1_ac1(self, data):
                    t_item = Model(**data['item'])
                    if t_item.save():
                        return True, 'Success!'
                    else:
                        return False, 'Error!'