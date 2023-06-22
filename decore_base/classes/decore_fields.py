import inspect
import logging
from pathlib import Path, PosixPath, WindowsPath
from shutil import move
from uuid import UUID

from peewee import (BooleanField, CharField, Field, ForeignKeyField,
                    IntegerField, ManyToManyField, MetaField, TextField,
                    UUIDField)
from pykeepass.entry import Entry

from ..globals import globals

__all__ = [
    'BackRefMetaField', 
    'BooleanField', 
    'CharField',
    'ForeignKeyField', 
    'IntegerField', 
    'ManyToManyField', 
    'PasswordField', 
    'TextField', 
    ]

class FileFieldAccessor(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            t_path = Path(globals.config['default']['state_path']).joinpath('filebase').joinpath(self.model.__name__).joinpath(instance.id).joinpath(self.name).joinpath(instance.__data__.get(self.name))
            if t_path.exists():
                return t_path.absolute()
            else:
                return None
        return self.field

    def __set__(self, instance, value):
        if instance.id:
            if type(value) == WindowsPath or type(value) == PosixPath:
                t_path = Path(globals.config['default']['state_path']).joinpath('filebase').joinpath(self.model.__name__).joinpath(instance.id).joinpath(self.name).joinpath(value.name)
                t_path.parent.mkdir(parents=True, exist_ok=True)
                move(value, t_path)
                instance.__data__[self.name] = value.name
            else:
                instance.__data__[self.name] = value
        else:
            logging.error('%s > %s' % (self.name, 'u can not store files while ur item id was not setted'))
            instance.__data__[self.name] = None
        instance._dirty.add(self.name)

class UUIDFieldAccessor(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            return instance.__data__.get(self.name)
        return self.field

    def __set__(self, instance, value):
        if isinstance(value, UUID):
            instance.__data__[self.name] = value
            instance._dirty.add(self.name)
        else:
            instance.__data__[self.name] = UUID(value) if value is not None else None
            instance._dirty.add(self.name)

class CustomField(Field):

    @property
    def instance(self):
        calling_frames = inspect.getouterframes(inspect.currentframe())
        for frame in calling_frames:
            instance = frame[0].f_locals.get('self')
            if isinstance(instance, self.model):
                return instance
        return None

class BackRefMetaField(MetaField):
    def __init__(self,verbose_name=None, help_text=None, filter_fields=None):
        super().__init__(False, False, False, None, None, False, None, None, None, False, None, help_text, verbose_name, None, None, False)
        self.filter_fields = filter_fields
    
    def bind(self, model, name, set_attribute):
        super().bind(model, name, set_attribute)
        setattr(model,'br_'+name, getattr(model, name)) 
        delattr(model, name)

class BooleanField(BooleanField):
    pass

class CharField(CharField):
    pass

class PasswordField(CustomField):
    field_type = 'VARCHAR'

    @property
    def kdb_group(self):
        t_group = globals.kdb.find_groups_by_name(self.model.__name__, group=globals.kdb.root_group, first=True)
        if not t_group:
            t_group = globals.kdb.add_group(globals.kdb.root_group, self.model.__name__)
            globals.kdb.save()
        return t_group

    def db_value(self, value):
        t_entry = None
        
        # MEMO - Suche nach einem Eintrag der dem Identifiziern entspricht 
        i_entry: Entry
        for i_entry in self.kdb_group.entries:
            if i_entry.title == self.name and i_entry.username == self.instance.id:
                t_entry = i_entry
        
        # MEMO - Wenn kein Eintrag vorhanden ist, lege einen neuen an und füge diesen der Gruppe hinzu
        if not t_entry:
            t_entry = Entry(title=self.name, username=self.instance.id, password=value, kp=globals.kdb)
            self.kdb_group.append(t_entry)
            try:
                globals.kdb.save()
            except:
                raise Exception('Could not save to keybase')
            
        # MEMO - Wenn der neue Wert nicht mit dem Password im Entry übereinstimmt und auch nicht mit der UUID dann ändere und speichere
        if not value == t_entry.password and not value == str(t_entry.uuid):
            t_entry.password = value
            try:
                globals.kdb.save()
            except:
                raise Exception('Could not save to keybase')
        
        # MEMO - schreibe die UUID des Entries in das __data__ Dict um das Kennwort zu verschleiern
        return str(t_entry.uuid)

    def python_value(self, value):
        t_entry = None
        
        # MEMO - Suche nach einem Eintrag der dem Identifiziern entspricht und gebe das Password des Eintrages zurück
        i_entry: Entry
        for i_entry in self.kdb_group.entries:
            if i_entry.uuid.hex == value:
                return i_entry.password
        
        # MEMO - Wenn kein Eintrag vorhanden ist, gebe None als Passwort aus
        if not t_entry:
            return None

class ForeignKeyField(ForeignKeyField):
    pass

class IntegerField(IntegerField):
    pass

class ManyToManyField(ManyToManyField):
    def __init__(self, model, backref=None, on_delete=None, on_update=None, _is_backref=False, verbose_name=None, help_text=None, filter_fields=None):
        super().__init__(model, backref, on_delete, on_update, _is_backref)
        self.verbose_name = verbose_name
        self.help_text = help_text
        self.filter_fields = filter_fields
    
class TextField(TextField):
    pass

class FileField(Field):
    accessor_class = FileFieldAccessor
    field_type = 'VARCHAR'

class UUIDField(UUIDField):
    accessor_class = UUIDFieldAccessor
