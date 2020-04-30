import falcon
from falcon import uri
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy import parse_message
from wechatpy.replies import TextReply,ImageReply,VoiceReply
from wechatpy import WeChatClient

class Connect(object):
    def on_get(self, req, resp):
        query_string = req.query_string
        # 数据格式是 signature=xxx&echostr=xxx&timestamp=xxx&nonce=xxx
        query_list = query_string.split('&')
        b = {}
        for i in query_list:
            b[i.split('=')[0]] = i.split('=')[1]
        try:
            check_signature(token='Zhou1234', signature=b['signature'],
            timestamp=b['timestamp'], nonce=b['nonce'])
            resp.body = (b['echostr'])
        except InvalidSignatureException:
            pass
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        # 猜测是打开数据流
        xml = req.stream.read()
        # 解析xml格式数据
        msg = parse_message(xml)
        if msg.type == 'text':
            reply = TextReply(content='露露我爱你', message=msg) # content=msg.content
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'image':
            reply = ImageReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200
        elif msg.type == 'voice':
            reply = VoiceReply(media_id=msg.media_id, message=msg)
            xml = reply.render()
            resp.body = (xml)
            resp.status = falcon.HTTP_200

    def on_aa(self, appid, secret):
        client = WeChatClient
#  AppID wx1ad36469789ff02d
#  #AppSecret 92a1d8c86f8df07554f6b6c6c19544ce
app = falcon.API()
connect = Connect()
app.add_route('/connect', connect)