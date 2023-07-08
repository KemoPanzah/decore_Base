from ..classes.decore_model import *
from ..globals import globals

from pathlib import Path

class Conform_model(Decore_model):
    
    def __init__(self, *args, **kwargs):
        Decore_model.__init__(self, *args, **kwargs)

    class Meta:
        # TODO - diese Zeile wieder einsetzen wenn alle Relationen zwischen conform und perform passen
        # database = SqliteDatabase('state/database.db', pragmas=(('cache_size', -1024 * 64),('journal_mode', 'wal')))
        db_path = Path(globals.config.state_path).joinpath('database.db')
        database = SqliteDatabase(db_path)

    @classmethod
    def register(cls):
        super(Conform_model, cls).register()
        cls.migrate_database()
        return cls