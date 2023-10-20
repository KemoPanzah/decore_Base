from flask_jwt_extended import JWTManager, create_access_token

from .decore_model import *


class Decore_mayor(Decore_model):
    username = CharField(null=False, unique=True, verbose_name='Username')
    password = CharField(verbose_name='Password')

    class Meta:
        database = SqliteDatabase('state/mayorbase.db')

    # Funktion um die Tabelle zu erstellen und die Klasse zurückzugeben
    @classmethod
    def register(cls, api):
        super(Decore_mayor, cls).register()
        cls.jwt = JWTManager(api)
        if cls.get_or_none(cls.username == 'guest') is None:
            guest = cls()
            guest.title = 'Guest'
            guest.username = 'guest'
            guest.password = 'guest'
            guest.save()

        return cls
    
    def login(self, request):
        return {'success': True, 'access_token': create_access_token(identity='guest')}, 200