from decore_base.uniform.conform_model import *

class Test_model(Conform_model):
    date = DateField(null=True, verbose_name="Date")
    datetime = DateTimeField(null=True, verbose_name="Datetime")
    password = PasswordField(null=True, verbose_name="Password")
