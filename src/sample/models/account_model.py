from decore_base.extensions.conform_model import *
from .person_model import Person_model

class Account_model(Conform_model):
    person = ForeignKeyField(Person_model, backref='accounts', verbose_name='Person')
    email = CharField(verbose_name='Email')
    password = PasswordField(verbose_name='Password')