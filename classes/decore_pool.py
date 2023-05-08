from .decore_base import Decore_base
from .decore_object import Decore_object
from .decore_view import Decore_view
from .decore_dialog import Decore_dialog
from .decore_widget import Decore_widget
from .decore_action import Decore_action
from .decore_element import Decore_element
from .decore_function import Decore_function
from .decore_list import Decore_list



import inspect
from peewee import Field


class Decore_pool(object):
    def __init__(self):
        self.__data__ = dict()
        self.base_s = []
        self.view_s = []
        self.dialog_s = []
        self.widget_s = []
        self.action_s = []
        self.element_s = []

    def register(self, p_instance):
        if not p_instance.id in self.__data__:
            self.__data__[p_instance.id] = p_instance
        else:
            raise Exception('instance with the same id already in pool')
    
    def extend(self):
        value: Decore_object
        for value in self.__data__.values():
            if Decore_base in inspect.getmro(value.__class__):
                if not self.__data__['app'].base_id:
                    self.__data__['app'].base_id = value.id
                self.__data__[value.parent_id].base_id_s.append(value.id)
                self.base_s.append(value)
            if Decore_view in inspect.getmro(value.__class__):
                if not self.__data__['app'].view_id:
                    self.__data__['app'].view_id = value.id
                self.__data__[value.parent_id].view_id_s.append(value.id)
                self.view_s.append(value)
            if Decore_dialog in inspect.getmro(value.__class__):
                self.__data__[value.parent_id].dialog_id_s.append(value.id)
                self.dialog_s.append(value)
            if Decore_widget in inspect.getmro(value.__class__):
                self.__data__[value.parent_id].widget_id_s.append(value.id)
                self.widget_s.append(value)
            if Decore_action in inspect.getmro(value.__class__):
                self.__data__[value.parent_id].action_id_s.append(value.id)
                self.action_s.append(value)
            if Decore_element in inspect.getmro(value.__class__):
                self.__data__[value.parent_id].element_id_s.append(value.id)
                self.element_s.append(value)
            if Decore_function in inspect.getmro(value.__class__):
                self.__data__[value.parent_id].function_s.append(value)

    def export(self):
        return self.serialize(self.__data__)

    def serialize(self, p_value):
        t_return = {}
        
        if type(p_value) is dict:
            for key, value in p_value.items():
                t_return[key] = self.serialize(value)
        elif Decore_object in inspect.getmro(p_value.__class__):
            setattr(p_value,'class', p_value.__class__.__name__)
            for key, value in p_value.__dict__.items():
                t_return[key] = self.serialize(value)
        elif Field in inspect.getmro(p_value.__class__):
            setattr(p_value,'class', p_value.__class__.__name__)
            for key, value in p_value.__dict__.items():
                # t_return['class'] = str(p_value)
                t_return[key] = self.serialize(value)
        # TODO - depricated - Decore_list wird nicht mehr benötigt - entferne aus dem gesamten Framework
        elif Decore_list in inspect.getmro(p_value.__class__):
            t_list = []
            for value in p_value:
                t_list.append(self.serialize(value))
            return t_list
        elif type(p_value) is list:
            t_list = []
            for value in p_value:
                t_list.append(self.serialize(value))
            return t_list
        elif type(p_value) is str or type(p_value) is bool or type(p_value) is int:
            return p_value
        elif not p_value:
            return None
        else:
            return str(p_value)
        
        return t_return

    def get_names(self):
        r_value = {}
        for base in self.base_s:
            for key, value in base.model.verbose_names.items():
                r_value[key] = value
        return r_value