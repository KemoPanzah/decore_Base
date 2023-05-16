from decore_base.extensions.conform_model import *

class Person_model(Conform_model):
    br_companies = BackRefMetaField(ref_name='companies', verbose_name='Companies')
    br_accounts = BackRefMetaField(ref_name='accounts', verbose_name='Accounts')
    first_name = CharField(verbose_name='First name')
    last_name = CharField(verbose_name='Last name')
    academic_degree = CharField(verbose_name='Academic degree')
    age = IntegerField(verbose_name='Age')
    capacity = IntegerField(verbose_name='Capacity', default=1)