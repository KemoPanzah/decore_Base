# fmt: off
import sys, os
#sys.path.append(os.path.abspath('../'))
# fmt: on

from .test_model import Test_model

# Testklasse für MyClass
class Test_fields:
    def setup_item(self):
        Test_model.create_table()
        self.test_item = Test_model()
        self.test_item.id = 'bcc2c3a4-1d52-11ee-9d5f-309c23812330'
        self.test_item.title = "Test Item"

    def test_password_field(self):
        self.setup_item()
        self.test_item.password = "12345678"
        self.test_item.save()
        db_item = Test_model.get(Test_model.id == self.test_item.id)

        assert self.test_item.password == '12345678'
        assert self.test_item.__data__['password'] != '12345678'
        assert db_item.password == "12345678"
        assert db_item.__data__['password'] != "12345678"