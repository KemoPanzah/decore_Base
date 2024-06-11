class Decore_route:
    def __init__ (self):
        self._mutaded = False
        self.__data__ = {'path':None, 'name':None, 'params':{'base_id':None, 'view_id':None, 'dialog_id':None, 'item_id':None, 'subdialog_id': None, 'subitem_id':None}}

    @property
    def path(self,):
        return self.__data__['path']

    @path.setter
    def path(self, value):
        self.__data__['path'] = value
        self._mutaded = True
    
    @property
    def name(self):
        return self.__data__['name']

    @name.setter
    def name(self, value):
        self.__data__['name'] = value
        self._mutaded = True
    
    @property
    def base_id(self):
        return self.__data__['params']['base_id']

    @base_id.setter
    def base_id(self, value):
        self.__data__['params']['base_id'] = value
        self._mutaded = True
    
    @property
    def view_id(self):
        return self.__data__['params']['view_id']

    @view_id.setter
    def view_id(self, value):
        self.__data__['params']['view_id'] = value
        self._mutaded = True
    
    @property
    def dialog_id(self):
        return self.__data__['params']['dialog_id']

    @dialog_id.setter
    def dialog_id(self, value):
        self.__data__['params']['dialog_id'] = value
        self._mutaded = True

    @property
    def item_id(self):
        return self.__data__['params']['item_id']
    
    @item_id.setter
    def item_id(self, value):
        self.__data__['params']['item_id'] = value
        self._mutaded = True
    
    @property
    def subdialog_id(self):
        return self.__data__['params']['subdialog_id']

    @subdialog_id.setter
    def subdialog_id(self, value):
        self.__data__['params']['subdialog_id'] = value
        self._mutaded = True

    @property
    def subitem_id(self):
        return self.__data__['params']['subitem_id']
    
    @subitem_id.setter
    def subitem_id(self, value):
        self.__data__['params']['subitem_id'] = value
        self._mutaded = True

    def get(self):
        if self._mutaded:
            return self.__data__
        else:
            return None