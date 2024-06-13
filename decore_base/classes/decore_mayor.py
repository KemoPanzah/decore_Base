from pathlib import Path

import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity

from .decore_model import *


class Decore_mayor(Decore_model):

    username = CharField(unique=True, verbose_name='Username')
    password = PasswordField(verbose_name='Password')
    role = IntegerField(verbose_name='Role', default=1)

    class Meta:
        # TODO - diese Zeile wieder einsetzen
        # database = SqliteDatabase('state/database.db', pragmas=(('cache_size', -1024 * 64),('journal_mode', 'wal')))
        db_path = Path(globals.config.state_path).joinpath('database.db')
        database = SqliteDatabase(db_path)

    @classmethod
    def register(cls):
        super(Decore_mayor, cls).register()
        cls.migrate_database()
        return cls

    @classmethod
    def hash_password(cls, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @classmethod
    def check_password(cls, password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    
    @classmethod
    def get_account_from_identity(cls, p_identity):
        t_account = cls.get_or_none(cls.username == p_identity)
        if t_account is None:
            return None
        else:
            return t_account

    # @classmethod
    # def get_token(cls, username, password, p_expires_delta=None):
    #     t_account = cls.get_or_none(cls.username == username)
 
    #     if not t_account is None and cls.check_password(password, t_account.password):
    #         return create_access_token(identity=t_account.username, expires_delta=p_expires_delta)
        
    #     return None
    
    def __init__(self, *args, **kwargs):
        Decore_model.__init__(self, *args, **kwargs)
        self.token = None

    def set_token(self, password, p_expires_delta=None):
        if self.check_password(password, self.password):
            self.token = create_access_token(identity=self.username, expires_delta=p_expires_delta)
        else:
            self.token = None