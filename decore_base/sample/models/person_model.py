from decore_base.uniform import *

class Person_model(Conform_model):
    companies = BackRefMetaField(verbose_name='Companies')
    accounts = BackRefMetaField(verbose_name='Accounts')
    first_name = CharField(verbose_name='First name')
    last_name = CharField(verbose_name='Last name')
    academic_degree = CharField(verbose_name='Academic degree')
    age = IntegerField(verbose_name='Age')
    capacity = IntegerField(verbose_name='Capacity', default=1)