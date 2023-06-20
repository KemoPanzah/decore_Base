from ..globals import globals
from .decore_object import Decore_object

import secrets
from pathlib import Path
from threading import Thread


class Decore_base(Decore_object):
    def __init__(self, p_id, p_icon, p_title, p_desc, p_model):
        Decore_object.__init__(self, p_id=p_id, p_parent_id='app', p_source_id=None, p_icon=p_icon, p_title=p_title, p_desc=p_desc, p_doc=None)
        self.model = p_model.register()
        self.field_s = p_model.field_s
        self.rel_field_s = p_model.rel_field_s
        self.schema = p_model.build_schema()
        self.function_s = []

    def start_shot(self):
        for i_function in self.function_s:
            if i_function.type == 'shot':
                i_function.func(self)

    def start_work(self):
        for i_function in self.function_s:
            if i_function.type == 'work':
                self.worker = Thread(target=self.work, daemon=True, name=self.__class__.__name__)
                self.worker.start()

    def work(self):
        while(True):
            for i_function in self.function_s:
                if i_function.type == 'worker':
                    i_function.func(self)

    # def create_secret(self):
    #     return (secrets.token_hex(2))

    # def create_path(self, p_id, mkdir=False):
    #     t_root_path = globals.config['default']['data_path']
    #     r_value: Path = Path(t_root_path).joinpath(self.id, p_id)
    #     if mkdir == True:
    #         r_value.mkdir(parents=True)
    #     return r_value.as_posix()