from decore_base.uniform.conform_model import *

class Test_model(Conform_model):
    charfield = CharField(verbose_name='CharField', default='Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
    intfield = IntegerField(verbose_name='IntegerField', default=0)
    textfield = TextField(verbose_name='TextField', default='Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.')
    booleanfield = BooleanField(verbose_name='BooleanField', default=False)
    passwordfield = PasswordField(verbose_name='PasswordField', default='12345678')