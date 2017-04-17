#coding=utf-8

from peewee import *
from flask import Flask
from playhouse.db_url import connect
from playhouse.pool import  PooledMySQLDatabase



#DATABASE = 'mysql://root:2wsx3edc@561731630d2d7.sh.cdb.myqcloud.com:10522/device_info'
DATABASE = 'mysql://root:123321@localhost:3306/device_info'
database = connect(DATABASE)



class BaseModel(Model):
    class Meta:
        database = database



class Device_Info(BaseModel):
    device_id = IntegerField(unique=True,primary_key=True)
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
    def get_dev_by_id(cls,id):
        data = Device_Info.select().where(Device_Info.device_id == id)
        return data

    class Meta:
        db_table = 'DEVICE_INFO'
        order_by = ('device_id',)
        indexes = (
            (('device_id'), True),
        )



class Device_Identifier(BaseModel):
    device = ForeignKeyField(Device_Info,related_name='identifier')
    imei = CharField()

    @classmethod
    def get_dev_by_imei(cls,imei):
        data = Device_Identifier.select().where(Device_Identifier.imei == imei)
        return data

    class Meta:
        db_table = 'DEVICE_IDENTIFIER'
        indexes = (
            (('device_id', 'imei'), True),
        )
        primary_key = CompositeKey('device_id', 'imei')

class Lend_Record(BaseModel):
    lend_id = IntegerField(unique=True,primary_key=True)
    device_id = IntegerField()
    out_time = DateTimeField()
    user_name = CharField()
    user_department = CharField()
    user_building = CharField()
    user_floor = CharField()
    user_room = CharField()
    status = CharField()
    return_time = DateTimeField()

    class Meta:
        db_table = 'LEND_RECORD'
        order_by = ('out_time',)
        indexes = (
            (('lend_id'), True),
        )

