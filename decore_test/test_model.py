from decore_base.uniform.conform_model import *

class Test_model(Conform_model):
    password = PasswordField(null=True, verbose_name="Password")
