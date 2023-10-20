from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
import bcrypt

from .decore_model import *


class Decore_mayor(Decore_model):
    username = CharField(unique=True, verbose_name='Username')
    password = CharField(verbose_name='Password')
    role = CharField(verbose_name='Role', default='guest')

    class Meta:
        database = SqliteDatabase('state/mayorbase.db')

    # Funktion um die Tabelle zu erstellen und die Klasse zurückzugeben
    @classmethod
    def register(cls, api):
        super(Decore_mayor, cls).register()
        cls.jwt = JWTManager(api)
        if cls.get_or_none(cls.username == 'guest@decore.base') is None:
            guest = cls()
            guest.title = 'Guest Account'
            guest.desc = 'Account to log in automatically as user with guest role'
            guest.username = 'guest@decore.base'
            guest.password = cls.hash_password('password')
            guest.save()
        return cls
    
    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @classmethod
    def login(cls, request):
        username = request.json['username']
        password = request.json['password']
        return {'success': True, 'access_token': create_access_token(identity='guest')}, 200