import json, logging, inspect

class Return_value(object):
    def __init__(self, p_success:bool, p_result, p_logging=True):
        self.__data__ = {'success': p_success, 'result': p_result}
        self.__json__ = {'success': p_success, 'result': str(p_result)}

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