from decore_base import decore
from models.test_model import Test_model

@decore.base(p_title='Test Base', p_icon='mdi-test-tube', p_model=Test_model)
class Test_base:
    @decore.view(p_title='Formtest', p_icon='mdi-test-tube', p_type='table')
    def tst_vi1():
        @decore.dialog(p_title='Formtest', p_icon='mdi-test-tube', p_type='standard', p_activator='none')
        def tst_vi1_di1():
            pass