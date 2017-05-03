#coding=utf-8

from flask import Flask,request
from flask import render_template
from db import *

app = Flask(__name__)


# @app.before_request
# def _db_connect():
#     database.connect()
#
# @app.teardown_request
# def _db_close(exc):
#     if not database.is_closed():
#         database.close()

@app.route('/')
@app.route('/intro')
def intro():
    """
    介绍页面
    :return:
    """
    return render_template('intro.html')

@app.route('/d')
@app.route('/d/<int:id>',methods=['GET'])
def get_dev_info(id):
    """
    获取设备ID对应的设备信息
    :param id:
    :return:
    """
    data = []
    try:
        data = Device_Info.get_dev_by_id(id)
    except StandardError, e:
        print e
    return render_template('device_info.html',device_info = data,type = 'id')


@app.route('/s')
@app.route('/s/<q>',methods=['GET'])
def search(q):
    """
    搜索imei或者ID,获得信息
    :param q:
    :return:
    """
    status = request.args.get('status')
    data = Device_Info.get_devs_by_name(name=q,status=status)
    return render_template('device_info.html',device_info = data, type = 'id')

@app.route('/imei/<imei>',methods=['GET'])
def get_dev_info_by_imei(imei):
    return render_template('device_info.html',device_info = Device_Identifier.get_dev_by_imei(imei),type = 'imei')

@app.route('/d/<int:id>/lend',methods=['GET'])
def get_lend_page(id):
     data = Device_Info.get_dev_by_id(id)
     if data[0].status == 'IN':
         return render_template('device_lend.html',device = data[0])
     else:
         return render_template('result.html',result = u'这个设备已经借出')

@app.route('/d/<int:id>/lend',methods=['POST'])
def rent_dev(id):
    try:
        print request.form
        Lend_Record.lend_pending(device_id=id, user_name=request.form['user_name'],
                                       user_department=request.form['user_department'],
                                       user_building=request.form['user_building'],
                                       user_floor=request.form['user_floor'],user_room=request.form['user_room'])
        return render_template('result.html',result = u'预订成功,请填写申请表并签字,提交给管理员.')
    except StandardError, e:
        return render_template('result.html',result = u'出错了!')
        print e

if __name__ == '__main__':
    app.run(port=23333,debug=True)
