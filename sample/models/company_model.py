from decore_base.extensions.conform_model import *
from .person_model import Person_model

class Company_model(Conform_model):
    persons = ManyToManyField(Person_model, backref='companies', verbose_name='Persons')