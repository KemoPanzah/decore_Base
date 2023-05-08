import Pyro5.api
import logging

from ..globals import globals
from ..classes.decore_model import *

Pyro5.config.SSL = True
Pyro5.config.SSL_CACERTS = "./cert/ca.crt"
Pyro5.config.SSL_CLIENTCERT = "./cert/client.crt"
Pyro5.config.SSL_CLIENTKEY = "./cert/client.key"
print("SSL enabled (2-way).")


class Reform_client_model(Decore_model):

    client_id = CharField(verbose_name='Client ID', default=globals.config.app_id)

    def __init__(self, p_id=None, *args, **kwargs):
        Decore_model.__init__(self, p_id, *args, **kwargs)
        self.remote_model = self.connect()

    class Meta:
        database = SqliteDatabase('state/database.db')

    @classmethod
    def connect(cls):
        t_uri = 'PYRO:' + cls.__name__ + '@' + globals.config.server_addr + \
            ':' + str(globals.config.server_port)
        with Pyro5.api.Proxy(t_uri) as t_model:
            return t_model

    def save_item(self):
        t_existing_item = self.get_or_none(self.__class__.id == self.id)
        try:
            if super(Reform_client_model, self).save_item():
                if self.remote_model.save_item(self.__data__):
                    return True
                else:
                    raise Exception('cannot save instance on server')
            else:
                raise Exception('cannot save instance on client') 
        except Exception as error:
            logging.error('%s > %s' % ('save_item', error))
            if not t_existing_item:
                 self.delete_instance()
            return False

    def remove_item(self):
        if super(Reform_client_model, self).remove_item():
            try:
                if self.remote_model.remove_item(self.__data__):
                    return True
                else:
                    raise Exception('cannot delete instance on server')
            except Exception as error:
                logging.error('%s > %s' % ('save_item', error))
                self.save(force_insert=True)
                return False
        else:
            logging.error('%s > %s' % ('save_item', error))
            return False
