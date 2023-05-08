from peewee import *

class Decore_query(Model):
    id = CharField(primary_key=True, unique=True, verbose_name="ID")
    parent = ForeignKeyField('self', backref='children', null=True, verbose_name='Parent')
    base_id = CharField(verbose_name='Base id')
    view_id = CharField(verbose_name='View id')
    type = CharField(verbose_name='Query type', default='user')
    title = CharField(verbose_name='Title')
    key =CharField(verbose_name='Key')
    value = CharField(verbose_name='Value')
    to = CharField(verbose_name='To')
    depth = IntegerField(verbose_name='Depth', default=0)

    class Meta:
        database = SqliteDatabase('state/querybase.db')