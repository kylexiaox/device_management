# coding=utf-8

from peewee import *
from playhouse.db_url import connect
from datetime import datetime
from config import database
from api import app

# DATABASE = 'mysql://abc:passwd@host:3306/db_name'

@app.before_request
def _db_connect():
    database.connect()

@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()

class BaseModel(Model):
    class Meta:
        database = database


class Device_Info(BaseModel):
    device_id = IntegerField(unique=True, primary_key=True)
    project = CharField()
    category = CharField()
    device_name = CharField()
    device_type = CharField()
    status = CharField()
    belonger = CharField()
    dev_status = CharField()
    possession_building = CharField()
    possession_floor = CharField()
    possession_room = CharField()
    user_department = CharField()
    remarks = CharField()
    batch = CharField()
    provider = CharField()

    @classmethod
    def get_dev_by_id(cls, id):
        data = Device_Info.select().where(Device_Info.device_id == id)
        print "get ID "+str(id)
        return data

    @classmethod
    def get_devs_by_name(cls, name=None, status=None):
        basic_query = Device_Info.select()
        if name != None:
            basic_query = basic_query.where((Device_Info.device_name.contains(name)) | (Device_Info.device_type.contains(name)))
        if status != None:
            basic_query = basic_query.filter(Device_Info.status == status)
        return basic_query

    class Meta:
        db_table = 'DEVICE_INFO'
        order_by = ('device_id',)
        indexes = (
            (('device_id'), True),
        )


class Device_Identifier(BaseModel):
    device = ForeignKeyField(Device_Info, related_name='identifier')
    imei = CharField()

    @classmethod
    def get_dev_by_imei(cls, imei):
        data = Device_Identifier.select().where(Device_Identifier.imei.contains(imei))
        return data

    class Meta:
        db_table = 'DEVICE_IDENTIFIER'
        indexes = (
            (('device_id', 'imei'), True),
        )
        primary_key = CompositeKey('device_id', 'imei')


class Lend_Record(BaseModel):
    lend_id = IntegerField(unique=True, primary_key=True)
    device = ForeignKeyField(Device_Info,related_name='rent_device')
    out_time = DateTimeField()
    user_name = CharField()
    user_department = CharField()
    user_building = CharField()
    user_floor = CharField()
    user_room = CharField()
    status = CharField()
    return_time = DateTimeField()

    @classmethod
    @database.atomic()
    def lend_pending(cls, device_id, user_name, user_department, user_building, user_floor, user_room):
        database.begin()
        try:
            Lend_Record.insert(device=device_id, out_time=datetime.now(), user_name=user_name,
                                  user_department=user_department, user_building=user_building, user_floor=user_floor,
                                  user_room=user_room,status = 'lend_pending').execute()
            Device_Info.update(status ='lend-pending').where(Device_Info.device_id == device_id).execute()
        except StandardError, e:
            print e
            database.rollback()
            raise
        else:
            try:
                database.commit()
            except:
                database.rollback()
                raise

    @classmethod
    @database.atomic()
    def return_by_lend_id(cls,device_id):
        try:
            Lend_Record.update(status = 'returned',return_time=datetime.now()).execute()
            Device_Info.update(status='IN',user_name=u'储物柜',return_time=datetime.now()).where(Device_Info.device_id==device_id).excute()
        except StandardError,e:
            print e
            database.rollback()
            raise
        else:
            try:
                database.commit()
            except:
                database.rollback()
                raise





    class Meta:
        db_table = 'LEND_RECORD'
        order_by = ('out_time',)
        indexes = (
            (('lend_id'), True),
        )
