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
    
    def extend(self):
        value: Decore_object
        for value in self.__data__.values():
            if Decore_base in inspect.getmro(value.__class__):
                # if not self.__data__['app'].start_base_id and value.navigation!='hide':
                #     self.__data__['app'].start_base_id = value.id
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].base_id_s.append(value.id)
                self.base_s.append(value)
            if Decore_view in inspect.getmro(value.__class__):
                # if not self.__data__['app'].view_id:
                #     self.__data__['app'].view_id = value.id
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].view_id_s.append(value.id)
            if Decore_dialog in inspect.getmro(value.__class__):
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].dialog_id_s.append(value.id)
            if Decore_widget in inspect.getmro(value.__class__):
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].widget_id_s.append(value.id)
            if Decore_action in inspect.getmro(value.__class__):
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].action_id_s.append(value.id)
            if Decore_template in inspect.getmro(value.__class__):
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].template_id_s.append(value.id)
            if Decore_hook in inspect.getmro(value.__class__):
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].hook_id_s.append(value.id)
            if Decore_element in inspect.getmro(value.__class__):
                if value.role < self.__data__[value.parent_id].role:
                    value.role = self.__data__[value.parent_id].role
                value.parent_kind = self.__data__[value.parent_id].kind
                # self.__data__[value.parent_id].element_id_s.append(value.id)
            if Decore_function in inspect.getmro(value.__class__):
                self.__data__[value.parent_id].function_s.append(value)

    def export(self, p_role, p_mode='all'):
        t_export_dict = {}
        for key, value in self.__data__.items():
            if p_role >= value.role:
                if p_mode == 'all':
                    t_export_dict[key] = value.export()
                elif p_mode == 'changed' and value.changed:
                    t_export_dict[key] = value.export()
        return t_export_dict

    

    # def get_names(self):
    #     r_value = {}
    #     for base in self.base_s:
    #         for key, value in base.model.verbose_names.items():
    #             r_value[key] = value
    #     return r_value