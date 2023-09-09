import json
from datetime import datetime

from peewee import (AutoField, BooleanField, CharField, DateTimeField,
                    IntegerField, Model, SqliteDatabase)

from .decore_action import Decore_action
from .decore_base import Decore_base


class Pool_actor(Model):
    
    active_s = []

    id = AutoField(primary_key=True)
    title = CharField()
    desc = CharField(null=True)
    finished = BooleanField(default=False)
    progress = IntegerField(default=0)
    success = BooleanField(default=False)
    result = CharField(null=True)
    created_at = DateTimeField(default=datetime.now)
    finished_at = DateTimeField()

    class Meta:
        database = SqliteDatabase('state/actorbase.db')
    
    # Funktion um die Tabelle zu erstellen und die Klasse zurückzugeben
    @classmethod
    def register(cls):
        cls.create_table(safe=True)
        return cls
    
    @classmethod
    def export_active_s(cls):
        r_value = []
        for i_active in cls.active_s:
            if not i_active.finished:
                r_value.append(i_active.__data__)
        return r_value
    
    @classmethod
    def export_item_s(cls):
        r_value = []
        for i_item in cls.select():
            r_value.append(i_item.__data__)
        return r_value        

    # Funktion um einen Actor-Entry zu erstellen und in die aktive Liste zu schreiben
    @classmethod
    def create_active(cls, p_title, p_desc):
        t_active = cls()
        t_active.title = p_title
        t_active.desc = p_desc
        cls.active_s.append(t_active)
        return t_active

    # Funktion um ein Item aus den Request-Daten zu erhalten, wenn kein Item im Request ist wird None zurückgegeben
    @classmethod
    def get_item(cls, p_model, p_dict):
        r_item = None
        if p_dict:
            r_item = p_model.get_or_none(p_model.id == p_dict['id'])
            if not r_item:
                r_item = p_model()
            
            r_item.update(p_dict)
        
        return r_item
   
    @classmethod
    def fire(cls, p_base:Decore_base, p_action:Decore_action, p_request):
        t_active = cls.create_active(p_action.title, p_action.desc)

        t_data = dict()
        t_item = None
        t_select_s = []
        
        if p_action.type == 'standard':
            t_data.update(json.loads(p_request.data))
            t_item = cls.get_item(p_base.model, t_data[p_action.parent_id]['item'])
            t_select_s = t_data[p_action.parent_id]['select_s']
        
        elif p_action.type == 'submit':
            t_data.update(json.loads(p_request.data))
            t_item = cls.get_item(p_base.model, t_data[p_action.parent_id]['item'])
            t_select_s = t_data[p_action.parent_id]['select_s']

        else:
            return {'success': False, 'result': 'Action type ('+ p_action.type +') not supported', 'errors':{}}, 200

        t_return = p_action.func(p_base, data=t_data, item=t_item, select_s=t_select_s, active=t_active)
        t_active.finish(t_return[0], t_return[1])
        return {'success': t_return[0], 'result': str(t_return[1]), 'errors':{}}, 200


    def finish(self, p_success, p_result):
        self.success = p_success
        self.result = p_result
        self.finished = True
        self.finished_at = datetime.now()
        self.save(force_insert=True)
        