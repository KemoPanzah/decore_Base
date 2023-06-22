from decore_base.uniform import *
from .person_model import Person_model

class Account_model(Conform_model):
    person = ForeignKeyField(Person_model, backref='accounts', verbose_name='Person', null=True)
    email = CharField(verbose_name='Email')
    password = PasswordField(verbose_name='Password')