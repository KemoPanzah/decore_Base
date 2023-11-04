import inspect
import logging
import operator
from functools import reduce
from uuid import uuid1

from cerberus import Validator
from peewee import CharField as _CharField
from peewee import DQ, FieldAccessor, Model, SqliteDatabase
from playhouse.migrate import SqliteMigrator, migrate
from playhouse.reflection import Introspector
from playhouse.shortcuts import model_to_dict


from ..globals import globals
from .decore_fields import *

from .model_validator import Model_validator
from .decore_translate import Decore_translate as t

class IDField(_CharField):
    pass

class Decore_model(Model):
    id = IDField(primary_key=True, unique=True, verbose_name="ID")
    owner_id = CharField(verbose_name=t('Owner ID'), null=True, default=None)
    title = CharField(verbose_name=t('Title'))
    desc = CharField(verbose_name=t('Description'), null=True)
    
    class Meta:
        # tbase = SqliteDatabase('state/database.db', pragmas=(('cache_size', -1024 * 64),('journal_mode', 'wal')))
        database = None
        tbase = SqliteDatabase('state/database.db')
        migrator = SqliteMigrator(database)
        user_query = {}

    def __init__(self, *args, **kwargs):
        Model.__init__(self, *args, **kwargs)     
        self.validator = Model_validator(self.__class__, self.build_schema(), allow_unknown = True)
        self.backref_stage = {}
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
    
    # @classmethod
    # @property
    # def full_field_s(cls):
    #     r_value = []
    #     for value in cls.__dict__.values():
    #         if FieldAccessor in inspect.getmro(value.__class__):
    #             r_value.append(value.field)
    #     return r_value
    
    # @classmethod
    # @property
    # def verbose_names(cls):
    #     r_value = {}
    #     for field in cls.full_field_s:
    #         if not hasattr(field, 'ref_name') and hasattr(field, 'verbose_name'):
    #             r_value[field.name] = str(field.verbose_name)
    #         elif hasattr(field, 'ref_name'):
    #             r_value[field.ref_name] = str(field.verbose_name)
    #     return r_value

    @classmethod
    def build_schema(cls):
        t_schema = {}
        for i_field in cls.field_s:
            t_schema[i_field.name] = {'nullable': i_field.null}

            if 'BooleanField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'boolean'

            if 'CharField' in i_field.__class__.__name__:
                t_schema[i_field.name]['empty'] = i_field.null
                t_schema[i_field.name]['type'] = 'string'
                t_schema[i_field.name]['unique'] = i_field.unique
                t_schema[i_field.name]['maxlength'] = i_field.max_length

            if 'DateField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'date'

            if 'DateTimeField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'datetime'

            if 'FloatField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'float'

            if 'ForeignKeyField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'dict'

            if 'IntegerField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'integer'

            if 'PasswordField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'string'

            if 'TextField' in i_field.__class__.__name__:
                t_schema[i_field.name]['type'] = 'string'

        return t_schema

    @classmethod
    def query(cls, p_query={}):
        r_item_s = cls.select()
        t_mm_query = {}
        t_uq_query = {}
        for key, value in p_query.items():         
            t_query_attr_s = key.split('__')
            t_field = t_query_attr_s[0]
            if t_field in cls._meta.manytomany.keys():
                t_rel_field = t_query_attr_s[1]
                t_operator =  t_query_attr_s[2]                
                t_mm_query.setdefault(t_field, []).append({'operator': t_operator, 'field': t_rel_field,  'value': value})
            elif t_field in cls._meta.user_query.keys():
                t_operator =  t_query_attr_s[1]
                t_uq_query.setdefault(t_field, []).append({'operator': t_operator, 'value': value})
            else:
                if type(value) is list:
                    t_exp = None
                    for item in value:
                        t_exp |= DQ(**{key: item})
                    r_item_s = r_item_s.filter(t_exp)

                elif type(value) is str or int or float or bool:
                    r_item_s = r_item_s.filter(**{key: value})
                else:
                    raise Exception('Type error in query value')
        
        for key, value in t_mm_query.items():   
            t_through_model = cls._meta.manytomany[key]._through_model
            t_rel_model = cls._meta.manytomany[key].rel_model
            r_item_s = r_item_s.join(t_through_model).join(t_rel_model)
            for i_attrs in value:
                t_operator = getattr(operator, i_attrs['operator'])
                t_field = i_attrs['field']
                t_value = i_attrs['value']
                if type(t_value) is list:
                    t_clause_s = []
                    for item in t_value:
                        t_clause_s.append(t_operator(getattr(t_rel_model, t_field), item))
                    t_exp = reduce(operator.or_, t_clause_s)
                    r_item_s = r_item_s.where(t_exp)
                elif type(t_value) is str or int or float or bool:
                    r_item_s = r_item_s.where(t_operator(getattr(t_rel_model, t_field),t_value))
                else:
                    raise Exception('Type error in query value')
                
        for key, value in t_uq_query.items():
            for i_attrs in value:
                r_item_s = cls._meta.user_query[key](cls, r_item_s, getattr(operator, i_attrs['operator']), i_attrs['value'])

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
        for i_item in t_item_s:
            t_item = i_item.__data__
            for i_field in cls.field_s:
                if type(i_field) == ForeignKeyField:
                    if t_item[i_field.name] in t_rel[i_field.name].keys():
                        t_item[i_field.name]=t_rel[i_field.name][t_item[i_field.name]]

            for i_rel_field in cls.rel_field_s:
                if 'ForeignKeyField' in i_rel_field.__class__.__name__:
                    t_item[i_rel_field.backref] = getattr(i_item, i_rel_field.backref).count()
                elif 'ManyToManyField' in i_rel_field.__class__.__name__:
                    t_item[i_rel_field.name] = getattr(i_item, i_rel_field.name).count()
            
            if not t_item in t_dict_s:
                t_dict_s.append(t_item)
        
        return {'item_s': t_dict_s, 'count': t_item_s.count()}

    @classmethod
    def get_attributed_value_s(cls, p_query, p_attr, p_rel_attr):
        r_value = {}
        t_item_s = cls.query(p_query)
        if p_attr:
            for item in t_item_s:
                if p_rel_attr:
                    t_attr = getattr(item, p_attr) 
                    #TODO - Hier bitte auf iterable prüfen und nicht auf exception setzen
                    try:
                        for rel_item in t_attr:
                            t_value = rel_item.__data__[p_rel_attr]
                            r_value[str(t_value)] = t_value

                    except TypeError as error:
                        t_value = t_attr.__data__[p_rel_attr]
                        r_value[str(t_value)] = t_value
                else:
                    t_value = item.__data__[p_attr]
                    r_value[str(t_value)] = t_value
            
            return r_value
        else:
            return r_value

    @classmethod
    def get_minified_dict_s(cls, p_query):
        r_value = []
        t_item_s = cls.query(p_query)
        for i_item in t_item_s:
            r_value.append({'id': i_item.id, 'title': i_item.title})
        return r_value

    @property
    def errors(self):
        self.validator.validate(self.to_dict())
        return self.validator.errors

    def validate(self):
        r_value =  self.validator.validate(self.to_dict())
        if r_value == False:
            logging.error('%s > %s' % ('validate_model', str(self.validator.errors)))
        return r_value

    # TODO - Wer ruft das auf? was ist damit?
    # def to_dict(self):
    #     return model_to_dict(self, recurse=True, max_depth=1)

    def from_dict(self, p_dict):
        for field in self.field_s:
            if field.name in p_dict.keys():
                if 'ForeignKeyField' in field.__class__.__name__:
                    if not p_dict[field.name] == None:
                        setattr(self, field.name, p_dict[field.name]['id'])
                    else:
                        setattr(self, field.name, None)
                else:
                    setattr(self, field.name, p_dict[field.name])
        
        for field in self.rel_field_s:
            if field.backref in p_dict.keys() and 'ForeignKeyField' in field.__class__.__name__:
                self.backref_stage[field.backref] = p_dict[field.backref]
            
            elif field.name in p_dict.keys() and 'ManyToManyField' in field.__class__.__name__:
                self.backref_stage[field.name] = p_dict[field.name]

        
    def to_dict(self):
        r_value = {}
        for field in self.field_s:
            #MEMO - Namensabfrage ist relevat weil der überschriebene Klassen gibt die nicht auf type geprüft werden können
            if 'ForeignKeyField' in field.__class__.__name__:
                try:
                    fk_attr = getattr(self, field.name)
                    if fk_attr:
                        r_value[field.name] = {'id': fk_attr.id, 'title': fk_attr.title}
                    else:
                        r_value[field.name] = None
                except Exception as error:
                    r_value[field.name] = None
            else:
                r_value[field.name] = getattr(self, field.name)
             
        for field in self.rel_field_s:
            if 'ForeignKeyField' in field.__class__.__name__:
                br_attr = getattr(self, field.backref)
                if br_attr:
                    r_value[field.backref] = [{'id': item.id, 'title': item.title} for item in br_attr]
                else:
                    r_value[field.backref] = []
            elif 'ManyToManyField' in field.__class__.__name__:
                mm_attr = getattr(self, field.name)
                if mm_attr:
                    r_value[field.name] = [{'id': item.id, 'title': item.title} for item in mm_attr]
                else:
                    r_value[field.name] = []
                
        return r_value

    def save(self):
        #TODO - auf errors umstellen
        #TODO - auf dirty_fields umstellen
        r_value = 0

        if self.validate():
            t_item = self.__class__.get_or_none(self.__class__.id == self.id)
            if not t_item:
                try:
                    globals.keybase.commit(self.id)
                    super(Decore_model,self).save(force_insert=True)
                except Exception as error:
                    logging.error('%s > %s > %s' % ('save_item', 'Insert error', error))
                    r_value = 0
                else:
                    r_value = 1
            elif t_item:
                if not self.to_dict() == t_item.to_dict():
                    try:
                        globals.keybase.commit(self.id)
                        super(Decore_model, self).save()
                    except Exception as error:
                        logging.error('%s > %s > %s' % ('save_item', 'Update error', error))
                        r_value = 0
                    else:
                        r_value = 2
                else:
                    r_value = 3
        else:
            logging.error('%s > %s' % ('save_item', 'Validation error'))
            r_value = 0

        if r_value > 0 and self.backref_stage:
            for field in self.rel_field_s:
                if field.backref in self.backref_stage.keys() and 'ForeignKeyField' in field.__class__.__name__:
                    br_attr = getattr(self, field.backref)
                    t_dict_id_s, t_br_attr_id_s = [item['id'] for item in self.backref_stage[field.backref]], [item.id for item in br_attr]
                    t_remove_id_s, t_add_id_s = [item.id for item in br_attr if item.id not in t_dict_id_s], [item for item in t_dict_id_s if item not in t_br_attr_id_s]
                    for i_remove_id in t_remove_id_s:
                        t_item = field.model.get(field.model.id == i_remove_id)
                        if field.null:
                            setattr(t_item, field.name, None)
                            t_item.save()
                        else:
                            t_item.delete_instance()
                    for i_add_id in t_add_id_s:
                        t_item = field.model.get(field.model.id == i_add_id)
                        if not getattr(t_item, field.name):
                            setattr(t_item, field.name, self.id)
                            t_item.save()
                        else:
                            logging.error('%s > %s' % ('from_dict', 'ForeignKey not setable because field in use by ForeignKey from another entity'))

                #MEMO - Namensabfrage ist relevat weil der überschriebene Klassen gibt die nicht auf type geprüft werden können
                elif field.name in self.backref_stage.keys() and 'ManyToManyField' in field.__class__.__name__:
                    mm_attr = getattr(self, field.name)
                    t_dict_id_s, t_mm_attr_id_s = [item['id'] for item in self.backref_stage[field.name]], [item.id for item in mm_attr] 
                    t_remove_id_s, t_add_id_s = [item.id for item in mm_attr if item.id not in t_dict_id_s], [item for item in t_dict_id_s if item not in t_mm_attr_id_s]
                    mm_attr.remove(t_remove_id_s)
                    mm_attr.add(t_add_id_s)

            self.backref_stage = {}

        return r_value

    #TODO - return values prüfen; werden die eigentlich benötigt? > delete_instance
    def delete_instance(self):
        if super(Decore_model, self).delete_instance():
            return True
        else:
            logging.error('%s > %s' % ('remove_item', 'Remove error'))
            return False

    @classmethod    
    def user_query(cls):
        def wrapper(func):
            cls._meta.user_query[func.__name__] = func
            pass
        return wrapper