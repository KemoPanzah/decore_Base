import inspect
import logging
import operator
from functools import reduce
from uuid import uuid1

from cerberus import Validator
from peewee import DQ, FieldAccessor, Model, SqliteDatabase
from playhouse.migrate import SqliteMigrator, migrate
from playhouse.reflection import Introspector
from playhouse.shortcuts import model_to_dict

#
from ..globals import globals
from .decore_fields import *
#
from .decore_translate import Decore_translate as t


class Decore_model(Model):
    id = CharField(primary_key=True, unique=True, verbose_name="ID")
    title = CharField(verbose_name=t('Title'))
    desc = CharField(verbose_name=t('Description'), null=True)
    item_type = CharField(verbose_name=t('Item type'), default='object')
    parent_path = CharField(verbose_name=t('Parent path'), null=True)
    
    class Meta:
        # tbase = SqliteDatabase('state/database.db', pragmas=(('cache_size', -1024 * 64),('journal_mode', 'wal')))
        database = None
        tbase = SqliteDatabase('state/database.db')
        migrator = SqliteMigrator(database)

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)
        if not self.id:
            self.id = str(uuid1())

    @classmethod
    def register(cls):
        if cls._meta.database:
            cls.create_table(safe=True)
        for field in cls._meta.manytomany.values():
            through_model = field.get_through_model()
            cls._meta.tbase.create_tables([through_model])
        return cls

    @classmethod
    def migrate_database(cls):
        t_introspector = Introspector.from_database(cls._meta.database)
        t_database_model = t_introspector.generate_models(table_names=cls._meta.table_name)[cls._meta.table_name]
        
        for cls_field in cls._meta.fields.values():
            b_cls_field_found = False
            for db_field in t_database_model._meta.fields.values():
                if cls_field.column_name == db_field.column_name:
                    b_cls_field_found = True
                    break
            if not b_cls_field_found:
                migrate(cls._meta.migrator.add_column(cls._meta.table_name, cls_field.column_name, cls_field))
        
        if globals.flags.purge_unused_database_cols:
            for db_field in t_database_model._meta.fields.values():
                b_db_field_found = False
                for cls_field in cls._meta.fields.values():
                    if db_field.column_name == cls_field.column_name:
                        b_db_field_found = True
                        break
                if not b_db_field_found:
                    migrate(cls._meta.migrator.drop_column(cls._meta.table_name, db_field.column_name, cascade=False))

    @classmethod
    @property
    def field_s(cls):
        return list(cls._meta.fields.values())

    @classmethod
    @property
    def rel_field_s(cls):
        r_value = []
        for field in cls._meta.backrefs:
            if not 'Through' in field.model.__name__:
                r_value.append(field)
        for field in cls._meta.manytomany.values():
            r_value.append(field)
        return r_value
    
    @classmethod
    @property
    def full_field_s(cls):
        r_value = []
        for value in cls.__dict__.values():
            if FieldAccessor in inspect.getmro(value.__class__):
                r_value.append(value.field)
        return r_value
    
    @classmethod
    @property
    def verbose_names(cls):
        r_value = {}
        for field in cls.full_field_s:
            if not hasattr(field, 'ref_name') and hasattr(field, 'verbose_name'):
                r_value[field.name] = str(field.verbose_name)
            elif hasattr(field, 'ref_name'):
                r_value[field.ref_name] = str(field.verbose_name)
        return r_value

    @classmethod
    def build_schema(cls):
        t_schema = {}
        for i_field in cls.field_s:
            if i_field.field_type == 'UUID' and i_field.null == False:
                t_schema[i_field.name] = {'empty': False}

            if i_field.field_type == 'VARCHAR' and i_field.null == False:
                t_schema[i_field.name] = {'type': 'string'}

            if i_field.field_type == 'TEXT'and i_field.null == False:
                t_schema[i_field.name] = {'type': 'string'}

            if i_field.field_type == 'BOOL'and i_field.null == False:
                t_schema[i_field.name] = {'type': 'boolean'}

            if i_field.field_type == 'INT'and i_field.null == False:
                t_schema[i_field.name] = {'type': 'integer'}

            if i_field.field_type == 'DATETIME'and i_field.null == False:
                t_schema[i_field.name] = {'type': 'datetime'}

            if i_field.field_type == 'FLOAT'and i_field.null == False:
                t_schema[i_field.name] = {'type': 'float'}

        return t_schema

    @classmethod
    def query(cls, p_query={}):
        r_item_s = cls.select()
        t_mm_query = {}
        for key, value in p_query.items():         
            t_query_attr_s = key.split('__')
            t_field = t_query_attr_s[0]
            if t_field in cls._meta.manytomany.keys():
                t_rel_field = t_query_attr_s[1]
                t_operator =  t_query_attr_s[2]                
                t_mm_query.setdefault(t_field, []).append({'operator': t_operator, 'field': t_rel_field,  'value': value})
            else:
                if type(value) is list:
                    t_exp = None
                    for item in value:
                        t_exp |= DQ(**{key: item})
                    r_item_s = r_item_s.filter(t_exp)

                elif type(value) is str or int:
                    r_item_s = r_item_s.filter(**{key: value})
                else:
                    raise Exception('Type error in query value')
        
        for key, value in t_mm_query.items():   
            t_rel_model = cls._meta.manytomany[key].rel_model
            t_through_model = cls._meta.manytomany[key]._through_model
            r_item_s = r_item_s.join(t_through_model).join(t_rel_model)
            for i_attrs in value:
                t_operator = i_attrs['operator']
                t_field = i_attrs['field']
                t_value = i_attrs['value']
                if t_operator == 'eq':
                    if type(t_value) is list:
                        t_clause_s = []
                        for item in t_value:
                            t_clause_s.append((getattr(t_rel_model, t_field) == item))
                        t_exp = reduce(operator.or_, t_clause_s)
                        r_item_s = r_item_s.where(t_exp)
                    elif type(t_value) is str:
                        r_item_s = r_item_s.where(getattr(t_rel_model, t_field) == t_value)
                    else:
                        raise Exception('Type error in query value')
        
        return r_item_s

    @classmethod
    def get_dict_s(cls, p_query=None, p_pag=None):
        t_dict_s = []
        t_item_s = None
        
        #MEMO - Relationale Daten abrufen
        t_rel = {}
        for i_field in cls.field_s:
            if type(i_field) == ForeignKeyField:
                t_rel[i_field.name] = {}
                for i_value in i_field.rel_model.select().dicts():
                    t_rel[i_field.name][i_value['id']] = i_value
        
        #MEMO - Query anwenden
            t_item_s = cls.query(p_query)

        #MEMO - Items mit relationalen Daten erweitern
        for i_item in t_item_s.dicts():
            for i_field in cls.field_s:
                if type(i_field) == ForeignKeyField:
                    i_item[i_field.name]=t_rel[i_field.name][i_item[i_field.name]]
            
            if not i_item in t_dict_s:
                t_dict_s.append(i_item)
        
        return {'item_s': t_dict_s, 'count': t_item_s.count()}

    @classmethod
    def get_option_s(cls, p_query, p_attr, p_rel_attr):
        r_value = []
        t_item_s = cls.query(p_query)
        if p_attr:
            for item in t_item_s:
                if p_rel_attr:
                    t_attr = getattr(item, p_attr) 
                    #TODO - Hier bitte nach dem typen fragen und nicht auf exception setzen
                    try:
                        for rel_item in t_attr:
                            t_value = rel_item.__data__[p_rel_attr]
                            if not t_value in r_value:
                                r_value.append(t_value)
                    except TypeError as error:
                        t_value = t_attr.__data__[p_rel_attr]
                        if not t_value in r_value:
                            r_value.append(t_value)
                else:
                    t_value = item.__data__[p_attr]
                    if not t_value in r_value:
                        r_value.append(t_value)
            return r_value
        else:
            return r_value

    def validate(self):
        t_schema = self.build_schema()
        #TODO - Schema as property and Validator as attribute in model
        t_val = Validator(t_schema, require_all=True, allow_unknown = True)
        r_value =  t_val.validate(self.__data__)
        if r_value == False:
            logging.error('%s > %s' % ('validate_model', str(t_val.errors)))
        return r_value

    # TODO - Wer ruft das auf? was ist damit?
    def to_dict(self):
        return model_to_dict(self, recurse=True, max_depth=1)

    def save(self):
        #TODO - auf try except umstellen und raisen in validate.
        if self.validate():
            t_item = self.__class__.get_or_none(self.__class__.id == self.id)
            if not t_item:
                try:
                    globals.keybase.commit(self.id)
                    super(Decore_model,self).save(force_insert=True)
                except Exception as error:
                    logging.error('%s > %s > %s' % ('save_item', 'Insert error', error))
                    return False
                else:
                    return True
            elif t_item:
                t_data = {k: v for k, v in t_item.__data__.items() if v is not None}
                if not self.__data__ == t_data:
                    try:
                        globals.keybase.commit(self.id)
                        super(Decore_model, self).save()
                    except Exception as error:
                        logging.error('%s > %s > %s' % ('save_item', 'Update error', error))
                        return False
                    else:
                        return True
                else:
                    return True
        else:
            logging.error('%s > %s' % ('save_item', 'Validation error'))
            return False

    #TODO - return values prüfen; werden die eigentlich benötigt? > delete_instance
    def delete_instance(self):
        if super(Decore_model, self).delete_instance():
            return True
        else:
            logging.error('%s > %s' % ('remove_item', 'Remove error'))
            return False