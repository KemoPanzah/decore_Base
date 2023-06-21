import inspect
from uuid import UUID
from pykeepass.entry import Entry

from peewee import CharField, Field, UUIDField
from ..globals import globals

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

class DecoreCustomField(Field):

    @property
    def instance(self):
        calling_frames = inspect.getouterframes(inspect.currentframe())
        for frame in calling_frames:
            instance = frame[0].f_locals.get('self')
            if isinstance(instance, self.model):
                return instance
        return None

class DecoreCharField(CharField):
    pass

class DecoreUUIDField(UUIDField):
    accessor_class = UUIDFieldAccessor

class DecorePasswordField(DecoreCustomField):
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
            if i_entry.title == self.name and i_entry.username == self.instance.id.hex:
                t_entry = i_entry
        
        # MEMO - Wenn kein Eintrag vorhanden ist, lege einen neuen an und füge diesen der Gruppe hinzu
        if not t_entry:
            t_entry = Entry(title=self.name, username=self.instance.id.hex, password=value, kp=globals.kdb)
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
        return t_entry.uuid.hex

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