from decore_base.uniform import *
from mimesis import Person
from random import randrange

def get_random_age():
    return Person().age(minimum=16, maximum=64)

def get_random_capacity():
    return randrange(1, 3)

class Person_model(Conform_model):
    companies = BackRefMetaField(verbose_name='Companies')
    accounts = BackRefMetaField(verbose_name='Accounts')
    first_name = CharField(verbose_name='First name', default=Person().first_name)
    last_name = CharField(verbose_name='Last name', default=Person().last_name)
    academic_degree = CharField(verbose_name='Academic degree', default=Person().academic_degree)
    age = IntegerField(verbose_name='Age', default=get_random_age)
    capacity = IntegerField(verbose_name='Capacity', default=get_random_capacity)

    