# -*- coding:utf-8 -*-

import time
from flask import Flask,g,request,make_response
import hashlib
import xml.etree.ElementTree as ET
# from database import User_alter
app = Flask(__name__)
app.debug=True


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
        toUser = xml_rec.find('ToUserName').text
        fromUser = xml_rec.find('FromUserName').text
        content = xml_rec.find('Content').text
#***********************content is input***********************
#            """  this is your code"""
        arg = filter(lambda x:len(x) != 0,content.split(' '))
        if arg[0] == 'h':
            content = msg
        elif arg[0] == '1':
            content = arg[0]
            # if User_alter(fromUser,arg[1],arg[2]):
            #     content = FAIL
            # else:
            #     content = SUCCESS
        else:
            content = arg[0]
#*******************************output************************
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromUser,toUser,str(int(time.time())), content))
        response.content_type='application/xml'
        return response