from pathlib import Path

import bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity

from .decore_model import *


class Decore_mayor(Decore_model):

    username = CharField(unique=True, verbose_name='Username')
    password = CharField(verbose_name='Password')
    role = IntegerField(verbose_name='Role', default=0)

    class Meta:
        # TODO - diese Zeile wieder einsetzen wenn alle Relationen zwischen conform und perform passen
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

    @classmethod
    def login(cls, username, password):
        t_account = cls.get_or_none(cls.username == username)
        if t_account is None:
            return None
        elif cls.check_password(password, t_account.password):
            return create_access_token(identity=t_account.username)