import inspect
import logging
from pathlib import Path, PosixPath, WindowsPath
from shutil import move
from uuid import UUID
from datetime import datetime

from peewee import (
    BooleanField, 
    CharField, 
    DateField, 
    DateTimeField, 
    Field, 
    FloatField, 
    ForeignKeyField, 
    IntegerField, 
    ManyToManyField, 
    MetaField, 
    TextField, 
    TimeField, 
    UUIDField,
    )

from pykeepass.entry import Entry

from ..globals import globals

__all__ = [
    'BackrefMetaField', 
    'BooleanField', 
    'CharField',
    'DateField',
    'DateTimeField',
    'FloatField',
    'ForeignKeyField', 
    'IntegerField', 
    'ManyToManyField', 
    'PasswordField', 
    'TextField',
    ]

# class FileFieldAccessor(object):
#     def __init__(self, model, field, name):
#         self.model = model
#         self.field = field
#         self.name = name

#     def __get__(self, instance, instance_type=None):
#         if instance is not None:
#             t_path = Path(globals.config['default']['state_path']).joinpath('filebase').joinpath(self.model.__name__).joinpath(instance.id).joinpath(self.name).joinpath(instance.__data__.get(self.name))
#             if t_path.exists():
#                 return t_path.absolute()
#             else:
#                 return None
#         return self.field

#     def __set__(self, instance, value):
#         if instance.id:
#             if type(value) == WindowsPath or type(value) == PosixPath:
#                 t_path = Path(globals.config['default']['state_path']).joinpath('filebase').joinpath(self.model.__name__).joinpath(instance.id).joinpath(self.name).joinpath(value.name)
#                 t_path.parent.mkdir(parents=True, exist_ok=True)
#                 move(value, t_path)
#                 instance.__data__[self.name] = value.name
#             else:
#                 instance.__data__[self.name] = value
#         else:
#             logging.error('%s > %s' % (self.name, 'u can not store files while ur item id was not setted'))
#             instance.__data__[self.name] = None
#         instance._dirty.add(self.name)

# class UUIDFieldAccessor(object):
#     def __init__(self, model, field, name):
#         self.model = model
#         self.field = field
#         self.name = name

#     def __get__(self, instance, instance_type=None):
#         if instance is not None:
#             return instance.__data__.get(self.name)
#         return self.field

#     def __set__(self, instance, value):
#         if isinstance(value, UUID):
#             instance.__data__[self.name] = value
#             instance._dirty.add(self.name)
#         else:
#             instance.__data__[self.name] = UUID(value) if value is not None else None
#             instance._dirty.add(self.name)

# class FieldAccessorTemplate(object):
#     def __init__(self, model, field, name):
#         self.model = model
#         self.field = field
#         self.name = name

#     def __get__(self, instance, instance_type=None):
#         if instance is not None:
#             return instance.__data__.get(self.name)
#         return self.field

#     def __set__(self, instance, value):
#         instance.__data__[self.name] = value
#         instance._dirty.add(self.name)

def to_datetime(p_value, p_mode):
    r_value = None
    
    t_formats = [
        '%Y-%m-%d %H:%M:%S.%f',
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%d %H:%M', 
        '%Y-%m-%d %H', 
        '%Y-%m-%d'
        ]
    
    for i_format in t_formats:
        try:
            r_value = datetime.strptime(str(p_value), i_format)
        except Exception as error:
            continue
    
    if r_value:
        if p_mode == 'date':
            r_value = r_value.date()

        elif p_mode == 'time':
            r_value = r_value.time()

        elif p_mode == 'datetime':
            r_value = r_value

    return r_value


class DateFieldAccessor(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            if instance.__data__.get(self.name) is not None:
                return to_datetime(instance.__data__.get(self.name), 'date')
            else:
                return None
        return self.field

    def __set__(self, instance, value):
        instance.__data__[self.name] = value
        instance._dirty.add(self.name)

class DateTimeFieldAccessor(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            if instance.__data__.get(self.name) is not None:
                return to_datetime(instance.__data__.get(self.name), 'datetime')
            else:
                return None
        return self.field

    def __set__(self, instance, value):
        instance.__data__[self.name] = value
        instance._dirty.add(self.name)

class PasswordFieldAccessor(object):
    def __init__(self, model, field, name):
        self.model = model
        self.field = field
        self.name = name

    def __get__(self, instance, instance_type=None):
        if instance is not None:
            if instance.__data__.get(self.name) is not None:
                return globals.keybase.get_entry(self.model.__name__, instance.__data__.get(self.name))
            else:
                return None
        return self.field

    def __set__(self, instance, value):
        if value is not None:
            instance.__data__[self.name] = globals.keybase.append(self.model.__name__, instance.id, self.name, str(value))
        else:
            instance.__data__[self.name] = None
        instance._dirty.add(self.name)

######################################################################################################

class BackrefMetaField(MetaField):
    ''' 
    [[Das BackrefMetaField wird benötigt damit **decore Front** Beziehungen zwischen Modellen darstellen kann. Es kann z.B. dem Filter oder einem Formular zugewiesen werden. Es ist ein MetaField und erhält keine Spalte in der Datenbank]].

    Parameters:
        verbose_name (str): [[Ein vom Benutzer lesbarer Name für das Feld]].
        help_text (str): Zusätzlicher Text, der in **decore Front** angezeigt wird.
        filter_fields (list): Eine Liste vom Typ String. Es werden nur die angegebenen Felder im Filter angezeigt. Wenn `empty`, werden alle Felder angezeigt.
        choice_query (dict): Ein `dictonary`, das eine Abfrage enthält, die beim laden von Optionen (z.B. in Auswahlfeldern im Frontend) berücksichtigt wird. Die Abfrage muss sich auf das Referenzmodell beziehen.

    !!! warning
        [[Der Name des `BackRefMetaField` muss mit dem Wert des angegebenen `backref` Parameters im *ForeignKey* oder *ManyToMany* Feldes im Referenzmodell übereinstimmen.]] [[Im folgendem Beispiel ist der Name des `BackRefMetaField` gleich `accounts` und ebenso der Wert des *ForeignKey* `backref` Parameters.]]

    ```python
    class User(Conform_model):
        username = CharField(verbose_name='Username')
        accounts = BackRefMetaField(null=True, verbose_name='Accounts', choice_query={'domain__eq': 'example.com'}
    ```

    ```python
    class Account(Conform_model):
        user = ForeignKeyField(User, backref='accounts', null=True, verbose_name='User')
        prefix = CharField(verbose_name='Mail prefix')
        domain = CharField(verbose_name='Mail domain', default='example.com')
    ```

    '''
    def __init__(self, help_text=None, verbose_name=None, filter_fields=[], choice_query={}):
        MetaField.__init__(self, help_text=help_text, verbose_name=verbose_name)
        self.filter_fields = filter_fields
        self.choice_query = choice_query
        
    def bind(self, model, name, set_attribute):
        super(BackrefMetaField, self).bind(model, name, set_attribute)
        setattr(model,'br_'+name, getattr(model, name))

class BooleanField(BooleanField):
    '''
    A field to store boolean values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''
    def __init__(self, null=False, default=None, help_text=None, verbose_name=None):
        super().__init__(null=null, default=default, help_text=help_text, verbose_name=verbose_name)

class CharField(CharField):
    '''
    A field to store char values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool unique: If True, the field must be unique in database table. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''
    def __init__(self, null=False, unique=False, default=None, choices=None, help_text=None, verbose_name=None):
        super().__init__(null=null, unique=unique, default=default, choices=choices, help_text=help_text, verbose_name=verbose_name)

class DateField(DateField):
    '''
    A field to store date values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''

    accessor_class = DateFieldAccessor

    def __init__(self, null=False, default=None, help_text=None, verbose_name=None):
        super().__init__(null=null, default=default, help_text=help_text, verbose_name=verbose_name)

class DateTimeField(DateTimeField):
    '''
    A field to store datetime values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''

    accessor_class = DateTimeFieldAccessor

    def __init__(self, null=False, default=None, help_text=None, verbose_name=None):
        super().__init__(null=null, default=default, help_text=help_text, verbose_name=verbose_name)

class FloatField(FloatField):
    '''
    A field to store float values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''
    def __init__(self, null=False, default=None, help_text=None, verbose_name=None):
        super().__init__(null=null, default=default, help_text=help_text, verbose_name=verbose_name)

class PasswordField(Field):
    '''
    :warning 
        The keybase is a KeePass file and should be protected by setting the correct access rights (ACL).

    A field to store passwords in the keybase and to use them again.
    
    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.

    .. code-block:: python

        class User(Conform_model):
            password = PasswordField(null=False, verbose_name='Password')

    '''
    accessor_class = PasswordFieldAccessor
    field_type = 'VARCHAR'

    def __init__(self, null=False, help_text=None, verbose_name=None):
        Field.__init__(self, null=null, verbose_name=verbose_name, help_text=help_text)

class ForeignKeyField(ForeignKeyField):
    '''
    A field to represent a one-to-many relationship between two models.

    :param Model model: The model to which the relationship is to be established.
    :param str backref: The name of the field in the reference model that represents the relationship to the model.
    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param str verbose_name: A human-readable name for the field.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param list filter_fields: A List of type string. Only the speciefied fields will be displayed in the filter. If None, all fields will be displayed.
    :param dict choice_query: A dictonary containing a query to be used when querying choices (e.g. in selection fields in the frontend). The query always refers to the reference model.
    '''
    def __init__(self, model, backref=None, null=False, default=None, help_text=None, verbose_name=None, filter_fields=[], choice_query={}):
        super().__init__(model, backref=backref, null=null, default=default, help_text=help_text, verbose_name=verbose_name)
        self.filter_fields = filter_fields
        self.choice_query = choice_query

class IntegerField(IntegerField):
    '''
    A field to store integer values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''
    def __init__(self, null=False, default=None, choices=None, help_text=None, verbose_name=None):
        super().__init__(null=null, default=default, choices=choices, help_text=help_text, verbose_name=verbose_name)

class ManyToManyField(ManyToManyField):
    '''
    A field to represent a many-to-many relationship between two models. It is a MetaField and does not get a column in the database. However, a through model is created by decore Base, which represents the relationship between the two models.
    
    :param Model model: The model to which the relationship is to be established.
    :param str backref: The name of the field in the reference model that represents the relationship to the model.
    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param str verbose_name: A human-readable name for the field.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param list filter_fields: A List of type string. Only the speciefied fields will be displayed in the filter. If None, all fields will be displayed.
    :param dict choice_query: A dictonary containing a query to be used when querying choices (e.g. in selection fields in the frontend). The query always refers to the reference model.

    .. code-block:: python

        class Account(Conform_model):
            users = ManyToManyField(User, backref='accounts', null=True, verbose_name='Users')
            prefix = CharField(verbose_name='Mail prefix')
            domain = CharField(verbose_name='Mail domain', default='example.com')

    .. code-block:: python

        class User(Conform_model):
            username = CharField(verbose_name='Username')
            accounts = BackRefMetaField(null=True, verbose_name='Accounts', choice_query={'domain__eq': 'example.com'}

    '''
    def __init__(self, model, backref=None, help_text=None, verbose_name=None, filter_fields=[], choice_query={}):
        super().__init__(model, backref=backref)
        self.help_text = help_text
        self.verbose_name = verbose_name
        self.filter_fields = filter_fields
        self.choice_query = choice_query
    
class TextField(TextField):
    '''
    A field to store text values.

    :param bool null: If True, the field is allowed to be null. Defaults to False.
    :param bool default: The default value for the field. Defaults to None.
    :param str help_text: Additional text to be displayed in **decore Front**.
    :param str verbose_name: A human-readable name for the field.
    '''
    pass

# class FileField(Field):
#     accessor_class = FileFieldAccessor
#     field_type = 'VARCHAR'

# class UUIDField(UUIDField):
#     accessor_class = UUIDFieldAccessor
