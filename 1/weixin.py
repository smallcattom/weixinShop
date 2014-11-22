import time
from flask import Flask,g,request,make_response
import hashlib
import xml.etree.ElementTree as ET
app = Flask(__name__)
app.debug=True
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
# '''  this is your code'''

#*******************************output************************
        xml_rep = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
        response = make_response(xml_rep % (fromUser,toUser,str(int(time.time())), content))
        response.content_type='application/xml'
        return response