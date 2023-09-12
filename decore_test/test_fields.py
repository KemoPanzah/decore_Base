import sys, os
from datetime import date, datetime


from .test_model import Test_model

# Testklasse für MyClass
class Test_fields:
    
    @classmethod
    def setup_class(cls):
        Test_model.create_table()

    def setup_method(self):
        self.test_item = Test_model()
        self.test_item.id = 'bcc2c3a4-1d52-11ee-9d5f-309c23812330'
        self.test_item.title = "Test Item"

    def test_date_field(self):
        self.test_item.date = "2021-01-01"
        assert isinstance(self.test_item.date, date)

        self.test_item.date = date(2021, 1, 1)
        assert isinstance(self.test_item.date, date)

        self.test_item.date = "2021-01"
        assert self.test_item.date == None

    def test_datetime_field(self):
        self.test_item.datetime = "2021-01-01 00:00:00"
        assert isinstance(self.test_item.datetime, datetime)

        self.test_item.datetime = "2021-01-01 00:00"
        assert isinstance(self.test_item.datetime, datetime)

        self.test_item.datetime = "2021-01"
        assert self.test_item.datetime == None


    def test_password_field(self):
        self.test_item.password = "12345678"
        self.test_item.save()
        db_item = Test_model.get(Test_model.id == self.test_item.id)

        assert self.test_item.password == '12345678'
        assert self.test_item.__data__['password'] != '12345678'
        assert db_item.password == "12345678"
        assert db_item.__data__['password'] != "12345678"


    @classmethod
    def teardown_class(cls):
        Test_model.drop_table()