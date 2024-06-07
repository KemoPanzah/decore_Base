class Decore_route(dict):
    def __init__ (self):
        self['name'] = None
        self['params'] = {'base_id':None, 'view_id':None, 'dialog_id':None, 'item_id':None, 'subdialog_id': None, 'subitem_id':None}
