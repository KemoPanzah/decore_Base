import logging, inspect

from pathlib import Path

class Decore_return(object):
    def __init__(self, p_success:bool, p_result, p_logging=True):
        self.__data__ = {'success': p_success, 'result': p_result, 'type': 'default'}

        t_of = inspect.getouterframes(inspect.currentframe())
        t_func = t_of[1].function

        if not p_success and p_logging:
            logging.error('%s > %s' % (t_func, p_result))

    @property
    def success (self):
        return self.__data__['success']

    @property 
    def result (self):
        return self.__data__['result']

    @property 
    def type (self):
        return self.__data__['type']

    def as_text(self):
        self.__data__['result'] = str(self.__data__['result'])
        self.__data__['type'] = 'text'
        return self
    
    def as_file(self):
        t_path = Path(self.__data__['result'])
        self.__data__['result'] = {'name': t_path.name, 'path': t_path.as_posix()}
        self.__data__['type'] = 'file'
        return self
