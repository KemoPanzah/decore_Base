from datetime import date, datetime
from json import dumps, loads

from decore_base.uniform.conform_model import *

class FKModel(Conform_model):
    pass

class Model(Conform_model):
    booelean = BooleanField()
    charfield = CharField()
    date = DateField()
    datetime = DateTimeField()
    floatfield = FloatField()
    foreignkey = ForeignKeyField(FKModel)
    integerfield = IntegerField()
    password = PasswordField()
    textfield = TextField()

class Test_model:
    
    obligatory_fields = 0

    @classmethod
    def setup_class(cls):
        Model.create_table()
        FKModel.create_table()

        for field in Model.field_s:
            if field.null == False:
                cls.obligatory_fields += 1

    @classmethod
    def teardown_class(cls):
        Model.drop_table()
        FKModel.drop_table()

    def setup_method(self):
        
        self.fk_item = FKModel()
        self.fk_item.id = 'b93a739d-5249-11ee-ae5b-c2ff292859a4'
        self.fk_item.title = "Test FK Item"
        self.fk_item.save()

        self.item = Model()
        self.item.id = 'bcc2c3a4-1d52-11ee-9d5f-309c23812330'
        self.item.title = "Test Item"
        self.item.booelean = True
        self.item.charfield = "char char baby"
        self.item.date = date(2021, 1, 1)
        self.item.datetime = datetime(2021, 1, 1, 0, 0, 0)
        self.item.floatfield = 1.0
        self.item.foreignkey = self.fk_item
        self.item.integerfield = 1
        self.item.password = "12345678"
        self.item.textfield = "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore"

    def teardown_method(self):
        self.item.delete_instance()

    def test_datefield(self):
        self.item.date = "2021-01-01"
        assert isinstance(self.item.date, date)

        self.item.date = date(2021, 1, 1)
        assert isinstance(self.item.date, date)

        self.item.date = "2021-01"
        assert self.item.date == None

    def test_datetimefield(self):
        self.item.datetime = "2021-01-01 00:00:00"
        assert isinstance(self.item.datetime, datetime)

        self.item.datetime = "2021-01-01 00:00"
        assert isinstance(self.item.datetime, datetime)

        self.item.datetime = "2021-01"
        assert self.item.datetime == None

    def test_foreignkeyfield(self):
        self.item.foreignkey = self.fk_item
        assert isinstance(self.item.foreignkey, FKModel)

        self.item.foreignkey = 'b93a739d-5249-11ee-ae5b-c2ff292859a4'
        assert isinstance(self.item.foreignkey, FKModel)

    def test_passwordfield(self):
        self.item.password = "12345678"
        self.item.save()
        db_item = Model.get(Model.id == self.item.id)

        assert self.item.password == '12345678'
        assert self.item.__data__['password'] != '12345678'
        assert db_item.password == "12345678"
        assert db_item.__data__['password'] != "12345678"

    # def test_item_dirty_fields(self):
    #     # Teste ob alle obligatorischen Felder dirty sind
    #     assert len(self.item.dirty_fields) == self.obligatory_fields
    #     self.item.save()
    #     # Teste ob alle obligatorischen Felder nicht mehr dirty sind
    #     assert len(self.item.dirty_fields) == 0
    #     id = self.item.id
    #     self.item = None
    #     self.item:Model = Model.get_or_none(Model.id == id)
    #     assert len(self.item.dirty_fields) == 0

    # def test_item_from_dict(self):
    #     t_dict = self.item.to_dict()
    #     assert len(self.item.dirty_fields) == self.obligatory_fields
    #     self.item.save()
    #     self.item.from_dict(t_dict)
    #     assert True

    # def test_item_from_json(self):
    #     t_dict = loads(dumps(self.item.to_dict(), default=str))
    #     assert len(self.item.dirty_fields) == self.obligatory_fields
    #     self.item.save()
    #     self.item.from_dict(t_dict)
    #     assert True