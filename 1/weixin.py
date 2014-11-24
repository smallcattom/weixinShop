# -*- coding:utf-8 -*-
# from dbl import *
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
msg = '命令格式:\n用户个人信息修改:\n1 选项id  新内容     注：0：地址 1：名字 2：电话\n商品查找:\n2 商品名\n下单:\n3\n商品库存查询:\n4 商品名\n删除购物车商品:\n5 商品名 数量\n查看购物车:\n6\n添加购物车:\n7  商品名 数量\n留言:\n 8 留言'

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
        
        # if msgtype == "event":
        #     msgcontent = xml_rec.find('Event').text
        #     if msgcontent == "subscribe":
        #         msgcontent = '欢迎关注猫商城帐号\n'
        #     else:
        #         msgcontent = 'error'

        #     response = make_response(xml_rep % (fromUser,toUser,str(int(time.time())), msgcontent))
        #     response.content_type='application/xml'
        #     return response
#***********************content is input***********************
#            """  this is your code"""
        arg = filter(lambda x:len(x) != 0,content.split(' '))
        content = xml_rec.find('Content').text
        if arg[0] == 'h':
            content = msg
        elif arg[0] == '1': 
            if User_alter(fromUser,arg[1],arg[2],g):
                content = FAIL
            else:
                content = SUCCESS
        elif arg[0] == '2':
            arr = goods_search(arg[1],g)
            
        else:
            content = arg[0]
       
#*******************************output************************
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromUser,toUser,str(int(time.time())), content))
        response.content_type='application/xml'
        return response