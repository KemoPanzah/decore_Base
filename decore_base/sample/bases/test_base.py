from decore_base import decore
from models.test_model import Test_model

@decore.base(p_title='Test Base', p_icon='mdi-test-tube', p_model=Test_model)
class Test_base:
    @decore.view(p_title='Formtest', p_icon='mdi-test-tube', p_type='table')
    def tst_vi1():
        @decore.dialog(p_title='Formtest', p_icon='mdi-test-tube', p_type='standard', p_display='drawer', p_activator='none')
        def tst_vi1_di1():
            @decore.widget(p_title='Formtest', p_icon='mdi-test-tube', p_type='form', p_active_s=[Test_model.title,Test_model.desc, Test_model.charfield, Test_model.intfield, Test_model.textfield])
            def tst_vi1_di1_wi1():
                @decore.action(p_title='Submit', p_type='submit', p_icon='mdi-test-tube')
                def tst_vi1_di1_wi1_ac1(self, t_data):
                    return True, 'Success'