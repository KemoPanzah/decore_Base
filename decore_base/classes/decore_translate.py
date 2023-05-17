import json
from translate import Translator


class Decore_translate(object):
    __source_language__ = 'en'
    __output_language__ = 'de'
    __trans_language_s__ = ['de']

    __data__ = None
    __file_data__ = {}

    def __init__(self, p_string):
        self.load_data()
        self.id = p_string
        if not p_string in self.__data__:
            self.__data__[p_string] = {self.__source_language__: p_string}
            self.translate()
        self.save_data()

    def __str__(self):
        return self.__data__[self.id][self.__output_language__]

    def translate(self):
        for trans_language in self.__trans_language_s__:
            if not trans_language in self.__data__[self.id]:
                self.__data__[self.id][trans_language] = Translator(from_lang=self.__source_language__, to_lang=trans_language).translate(self.id)

    @property
    def output(self):
        return self.__data__[self.id][self.__output_language__]

    @classmethod
    def load_data(cls):
        if cls.__data__ is None:
            try:
                with open('language.json', 'r') as t_file:
                    cls.__data__ = json.load(t_file)
                    cls.__file_data__.update(cls.__data__)
            except FileNotFoundError:
                cls.__data__ = {}

    @classmethod
    def save_data(cls):
        if not cls.__data__ == cls.__file_data__:
            with open('language.json', 'w') as t_file:
                json.dump(cls.__data__, t_file, indent=4)
                cls.__file_data__.update(cls.__data__)
