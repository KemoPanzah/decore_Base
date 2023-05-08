from ..globals import globals
from .decore_object import Decore_object

import secrets
from pathlib import Path
from threading import Thread


class Decore_base(Decore_object):
    def __init__(self):
        Decore_object.__init__(self, p_id=None, p_parent_id='app', p_source_id=None, p_icon=None, p_title=None, p_desc=None, p_doc=None)
        self.model = None
        self.through_model = None
        self.field_s = None
        self.rel_field_s = None
        self.schema = None
        self.function_s = []

    def start_inits(self):
        for i_function in self.function_s:
            if i_function.type == 'init':
                i_function.func(self)

    def start_worker(self):
        for i_function in self.function_s:
            if i_function.type == 'worker':
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