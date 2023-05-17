from ..classes.decore_model import *

class Conform_model(Decore_model):
    
    def __init__(self, p_id=None, *args, **kwargs):
        Decore_model.__init__(self, p_id, *args, **kwargs)

    class Meta:
        # TODO - diese Zeile wieder einsetzen wenn alle Relationen zwischen conform und perform passen
        # database = SqliteDatabase('state/database.db', pragmas=(('cache_size', -1024 * 64),('journal_mode', 'wal')))
        database = SqliteDatabase('state/database.db')
        migrator = SqliteMigrator(database)

    @classmethod
    def register(cls):
        super(Conform_model, cls).register()
        cls.migrate_database()
        return cls