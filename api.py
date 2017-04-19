#coding=utf-8

from flask import Flask
from flask import render_template
from db import *

app = Flask(__name__)


@app.before_request
def _db_connect():
    database.connect()

@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()

@app.route('/')
@app.route('/intro')
def intro():
    return render_template('intro.html')

@app.route('/d')
@app.route('/d/<id>',methods=['GET'])
def get_dev_info(id):
    if id == None:
        return render_template('device_info.html')
    else:
        data = Device_Info.get_dev_by_id(id)
        return render_template('device_info.html',device_info = data,type = 'id')

@app.route('/imei/<imei>',methods=['GET'])
def get_dev_info_by_imei(imei):
    return render_template('device_info.html',device_info = Device_Identifier.get_dev_by_imei(imei),type = 'imei')


if __name__ == '__main__':
    app.run(port=23333,debug=True)
