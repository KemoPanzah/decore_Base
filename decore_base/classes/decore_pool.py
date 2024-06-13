from .decore_base import Decore_base
from .decore_object import Decore_object
from .decore_view import Decore_view
from .decore_dialog import Decore_dialog
from .decore_widget import Decore_widget
from .decore_action import Decore_action
from .decore_template import Decore_template
from .decore_hook import Decore_hook
from .decore_element import Decore_element
from .decore_function import Decore_function


import inspect

class Decore_pool(object):
    def __init__(self):
        self.__data__ = dict()
        self.base_s = []
    
    @property
    def app(self):
        return self.__data__['app']

    def register(self, p_instance):
        if not p_instance.id in self.__data__:
            self.__data__[p_instance.id] = p_instance
        else:
            raise Exception('instance with the same id already in pool')
    
    #TODO das muss eine rekuriv funktion werden, sonst werden die rollen nicht richtig vererbt
    def extend(self):
        value: Decore_object
        for value in self.__data__.values():
            
            if value.kind == 'app':
                value.parent_kind = 'root'
            
            elif value.kind == 'base':
                self.base_s.append(value)
                value.parent_kind = self.__data__[value.parent_id].kind
                self.__data__[value.parent_id].child_id_s.append(value.id)

            elif value.kind == 'dialog':
                value.parent_kind = self.__data__[value.parent_id].kind
                self.__data__[value.parent_id].child_id_s.append(value.id)
                if self.__data__[value.parent_id].kind == 'widget':
                    value.kind = 'subdialog'
            
            elif value.kind == 'function':
                self.__data__[value.parent_id].function_s.append(value)
                value.parent_kind = self.__data__[value.parent_id].kind
                self.__data__[value.parent_id].child_id_s.append(value.id)

            else:
                value.parent_kind = self.__data__[value.parent_id].kind
                self.__data__[value.parent_id].child_id_s.append(value.id)
        
    def set_roles(self, p_object):
        if not p_object.kind == 'app':
            if p_object.role < self.__data__[p_object.parent_id].role and not p_object.role == 0:
                p_object.role = self.__data__[p_object.parent_id].role
        for child_id in p_object.child_id_s:
            self.set_roles(self.__data__[child_id])

    def lock_objects(self):
        for value in self.__data__.values():
            value._locked = True

    def export(self, p_role, p_mode='all'):
        t_return = {}
        for key, value in self.__data__.items():
            if value.kind=='app' or value.role==0 or p_role >= value.role:
                if p_mode == 'all':
                    t_return[key] = value.export()
                elif p_mode == 'mutated' and value._mutated:
                    t_return[key] = value.export()
        return t_return

    

    # def get_names(self):
    #     r_value = {}
    #     for base in self.base_s:
    #         for key, value in base.model.verbose_names.items():
    #             r_value[key] = value
    #     return r_value