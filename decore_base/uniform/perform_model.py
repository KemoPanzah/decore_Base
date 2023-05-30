from dateutil import parser
from pathlib import Path
import json
import logging

from ..globals import globals
from ..classes.decore_model import *


class Perform_model(Decore_model):
    def __init__(self, p_id=None, *args, **kwargs):
        Decore_model.__init__(self, p_id, *args, **kwargs)
        # TODO - entfernen und in save_json direkt auf config .state_path
        self.json_path = Path(globals.config.state_path).joinpath('jsonbase').joinpath(self.__class__.__name__)

    class Meta:
        database = SqliteDatabase(':memory:', thread_safe=False, check_same_thread=False)

    @classmethod
    def register(cls):
        super(Perform_model, cls).register()
        cls.load_db()
        return cls

    @classmethod
    def load_db(cls):
        t_path = Path(globals.config.state_path).joinpath('jsonbase').joinpath(cls.__name__)
        for i_file in t_path.glob('*.json'):
            with open(i_file) as o_file:
                # t_item = dict_to_model(cls, json.load(o_file), ignore_unknown=True)
                t_load = json.load(o_file)
                t_item = cls(p_id=t_load['id'])
                for i_field in cls.field_s:
                    if i_field.name in t_load:
                        if i_field.field_type == 'DATETIME':
                            setattr(t_item, i_field.name, parser.parse(t_load[i_field.name]))
                        else:
                            setattr(t_item, i_field.name, t_load[i_field.name])
                t_item.save(save_to_json=False)

    def save_json(self):
        t_path: Path = self.json_path.joinpath(self.id + '.json')
        t_data = {k: v for k, v in self.__data__.items() if v is not None}
        try:
            t_path.parent.mkdir(parents=True, exist_ok=True)
            t_path.touch(exist_ok=True)
            with open(t_path, 'w') as o_file:
                json.dump(t_data, o_file, default=str, indent=4)
        except Exception as e_error:
            logging.error('%s > %s' % ('save_json', e_error))
            return False
        else:
            return True

    def delete_json(self):
        t_path: Path = self.json_path.joinpath(self.id + '.json')
        try:
            t_path.unlink()
        except Exception as e_error:
            return False
        else:
            return True

    def save(self, save_to_json=True):
        if super(Perform_model, self).save():
            if save_to_json:
                return self.save_json()

    def remove_item(self):
        if super(Perform_model, self).remove_item():
            return self.delete_json()
