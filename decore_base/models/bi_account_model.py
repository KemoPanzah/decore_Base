from ..uniform.conform_model import *

class BI_Account_model(Conform_model):
    username = CharField(unique=True, verbose_name='Username')
    password = CharField(verbose_name='Password')
    role = IntegerField(verbose_name='Role', default=0)