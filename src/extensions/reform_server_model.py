from ..globals import globals
from ..classes.decore_model import *

import Pyro5.api
from pathlib import Path

print(Path('./cert/server.crt').absolute())

Pyro5.config.SSL = True
Pyro5.config.SSL_REQUIRECLIENTCERT = True   # enable 2-way ssl
Pyro5.config.SSL_CACERTS = './cert/ca.crt'
Pyro5.config.SSL_SERVERCERT = './cert/server.crt'
Pyro5.config.SSL_SERVERKEY = './cert/server.key'


print('SSL enabled (2-way).')


@Pyro5.api.expose
class Reform_server_model(Decore_model):

    daemon = Pyro5.api.Daemon(host='0.0.0.0', port=globals.config.server_port)

    client_id = CharField(verbose_name='Client ID')

    def __init__(self, p_id=None, *args, **kwargs):
        Decore_model.__init__(self, p_id, *args, **kwargs)

    class Meta:
        database = SqliteDatabase('state/database.db')
        migrator = SqliteMigrator(database)

    @classmethod
    def register(cls):
        super(Reform_server_model, cls).register()
        cls.migrate_database()
        uri = cls.daemon.register(cls, cls.__name__)
        print('Ready. Object uri =', uri)
        return cls

    @classmethod
    def start_request_loop(cls):
        cls.daemon.requestLoop()

    def save_item(self, p_data=None):
        if p_data:
            self.__data__.update(p_data)
        return super(Reform_server_model, self).save_item()

    def remove_item(self, p_data=None):
        if p_data:
            self.__data__.update(p_data)
        return super(Reform_server_model, self).remove_item()