# fmt: off
import sys, os
#sys.path.append(os.path.abspath('../'))
# fmt: on

from decore_base.uniform.conform_model import *

class Test_model(Conform_model):
    password = PasswordField(null=True, verbose_name="Password")

# Testklasse für MyClass
class Test_fields:
    def setup_item(self):
        self.test_item = Test_model()
        self.test_item.id = 'bcc2c3a4-1d52-11ee-9d5f-309c23812330'
        self.test_item.title = "Test Item"

    def test_set_password_field(self):
        self.setup_item()

        assert self.test_item.password == None