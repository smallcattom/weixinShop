# -*- coding:utf-8 -*-
from dbl import *
import time
from flask import Flask,g,request,make_response
import hashlib
import xml.etree.ElementTree as ET
import MySQLdb
app = Flask(__name__)
app.debug=True

from sae.const import (MYSQL_HOST, MYSQL_HOST_S, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
@app.before_request
def before_request():
    g.db = MySQLdb.connect(MYSQL_HOST, MYSQL_USER, MYSQL_PASS, MYSQL_DB, port = int(MYSQL_PORT), charset = 'utf8')
@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'): g.db.close()

SUCCESS = 'Success'
FAIL = 'Fail'
# h口令 对应的输出
msg = '命令格式:\n用户个人信息修改:\n1 选项id  新内容     注：0：地址 1：名字 2：电话\n商品查找:\n2 商品名\n下单:\n3 备注内容\n用户信息查询:\n4\n删除购物车商品:\n5 商品id 数量\n查看购物车:\n6\n添加购物车:\n7  商品id 数量\n留言:\n 8 留言'
@app.route('/',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='shop'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        msgtype = xml_rec.find('MsgType').text
        toUser = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        '''对于第一次关注时的操作'''
        if msgtype == "event":
            msgcontent = xml_rec.find('Event').text
            if msgcontent == "subscribe":
                msgcontent = '欢迎关注猫商城\n爱猫猫就是爱自己^_^'
                User_add(fromUser,'xxx','xxx',100000,g.db.cursor())
            else:
                msgcontent = 'error'
            xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
            response = make_response(xml_rep % (fromUser,toUser,str(int(time.time())), msgcontent))
            response.content_type='application/xml'
            return response

#***********************content is input***********************
#            """  this is your code"""
        content = xml_rec.find('Content').text
        arg = filter(lambda x:len(x) != 0,content.split(' '))
        
        if arg[0] == 'h':
            content = msg
        elif arg[0] == '1': 
            if len(arg) != 3:
                content = '格式错误\n信息修改格式为：1 选项id 新内容'
            elif User_alter(fromUser,arg[1],arg[2],g):
                content = FAIL
            else:
                content = SUCCESS
        elif arg[0] == '2':
            if len(arg) != 2:
                content = '格式错误\n商品查找格式为：2 商品名'
            else:
                content = goods_search(arg[1],g.db.cursor())
        elif arg[0] == '3':
            if len(arg) != 2:
                content = '格式错误\n下单命令格式：3 备注内容'
            else:
                content = cart_buy(fromUser,arg[1],g)
                if content == 1:
                    content = '购物车没有商品待下单'
                else:
                    content = '下单成功'
        elif arg[0] == '4':
            if len(arg) != 1:
                content = '格式错误\n用户信息查找格式为：4'
            else:
                content = User_info(fromUser,g.db.cursor());
                if content == 1:
                    content = 'error'
        elif arg[0] == '7':
            if len(arg) != 3:
                content = '格式错误\n商品查找格式为：7 商品id 数量'
            elif cart_add(arg[1],int(arg[2]),fromUser,g):
                content = '添加购物车失败'
            else:
                content = '添加购物车成功'
        elif arg[0] == '6':
            if len(arg) != 1:
                content = '格式错误\n查看购物车格式为：6'
            else:
                content = cart_get(fromUser,g.db.cursor())
                if content == 1:
                    content = '购物车为空'
        elif arg[0] == '5':
            if len(arg) != 3:
                content = '格式错误\n删除购物车商品命令格式：5 商品id 数量'
            elif cart_del(arg[1],arg[2],fromUser,g):
                content = '删除失败'
            else:
                content = '成功'
        elif arg[0] == '8':
            if len(arg) == 1:
                content = '格式错误\n留言格式为：8 留言'
            else:
                content = '‘' + arg[1].encode('utf8') + '’\n 留言成功'
        else:
            content = '没有该命令，请输入命令h查找'
       
#*******************************output************************
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromUser,toUser,str(int(time.time())), content))
        response.content_type='application/xml'
        return response