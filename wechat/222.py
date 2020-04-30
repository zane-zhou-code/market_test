import tornado.web
import tornado.options
import tornado.httpserver
import tornado.ioloop
import hashlib
import xmltodict
import time
import tornado.gen
import json
import os
import requests

from tornado.web import RequestHandler
from tornado.options import options,define
from tornado.httpclient import AsyncHTTPClient,HTTPRequest

WECHAT_TOKEN = "Zhou1234"
WECHAT_APP_ID= "wxeda2653276985320" # wx1ad36469789ff02d  wxeda2653276985320
WECHAT_APP_SECRET= "d3cd6dae8134bb3eddd9390f9a44cd59" # c1dedb45c90b16ff43c392fd44655288 d3cd6dae8134bb3eddd9390f9a44cd59

define("port", default=8080, type=int, help="")

class AccessToken(object):
    """access_token辅助类"""
    _access_token = None # 私有化
    _create_time = 0
    _expires_in = 0

    @classmethod
    @tornado.gen.coroutine
    def update_access_token(cls):
        client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/cgi-bin/token?" \
        "grant_type=client_credential&appid=%s&secret=%s" % (WECHAT_APP_ID,WECHAT_APP_SECRET)
        resp = yield client.fetch(url)
        dict_data = json.loads(resp.body)
        if "errcode" in dict_data:
            raise Exception("wechat server error")
        else:
            cls._access_token = dict_data["access_token"]
            cls._expires_in = dict_data["expires_in"]
            cls._create_time = time.time()

    @classmethod
    @tornado.gen.coroutine
    def get_access_token(cls):
        if time.time() - cls._create_time > (cls._expires_in - 200): # 为了及时更新access_token
            # 向微信服务器请求access_token
            yield cls.update_access_token()
            raise tornado.gen.Return(cls._access_token)
        else:
            raise tornado.gen.Return(cls._access_token)



class WechatHandler(RequestHandler):
    """对接微信服务器"""
    def prepare(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")

        tmp = [WECHAT_TOKEN, timestamp, nonce]
        tmp.sort()  # 排序
        tmp = "".join(tmp)

        real_signature = hashlib.sha1(tmp.encode('utf-8')).hexdigest()  # 转义utf8并用sha1加密
        if signature != real_signature:
            self.send_error(403)

    def get(self):
        echostr = self.get_argument("echostr")
        self.write(echostr)
    """回复消息(文字、语言、图片)"""
    def post(self):
        xml_data = self.request.body
        req = xmltodict.parse(xml_data)["xml"]
        msg_type = req["MsgType"]
        if msg_type == 'text':
            resp = {
                "ToUserName":req.get("FromUserName", ""),
                "FromUserName":req.get("ToUserName", ""),
                "CreateTime":int(time.time()),
                "MsgType":"text",
                "Content":req.get("Content", "")
            }
        elif msg_type =='voice':
            resp = {
                "ToUserName": req.get("FromUserName", ""),
                "FromUserName": req.get("ToUserName", ""),
                "CreateTime": int(time.time()),
                "MsgType": "voice",
                "Voice": {
                    "MediaId":req.get("MediaId", "")
                }
            }
        elif msg_type =='image':
            resp = {
                "ToUserName": req.get("FromUserName", ""),
                "FromUserName": req.get("ToUserName", ""),
                "CreateTime": int(time.time()),
                "MsgType": "image",
                "Image": {
                        "MediaId":req.get("MediaId", "")
                    }
            }
        elif msg_type == 'event':
            if req["Event"] == 'subscribe':
                """用户关注的消息"""
                resp = {
                    "ToUserName": req.get("FromUserName", ""),
                    "FromUserName": req.get("ToUserName", ""),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": u"欢迎光临露浩的小屋~~"
                }
                if "EventKey" in req:
                    event_key = req["EventKey"]
                    scene_id = event_key[8:]
                    resp["Content"] = u"欢迎光临露浩的小屋~~%s次" % scene_id
            elif req["Event"] == 'SCAN':
                scene_id = req["EventKey"]
                resp = {
                    "ToUserName": req.get("FromUserName", ""),
                    "FromUserName": req.get("ToUserName", ""),
                    "CreateTime": int(time.time()),
                    "MsgType": "text",
                    "Content": u"扫描的是%s" % scene_id
                }
            else:
                resp = None
        else:
            resp = {
                "ToUserName": req.get("FromUserName", ""),
                "FromUserName": req.get("ToUserName", ""),
                "CreateTime": int(time.time()),
                "MsgType": "text",
                "Content": "I love you, lulu"
            }
        """判断是否回复是否为None"""
        if resp:
            resp_xml = xmltodict.unparse({"xml": resp})
        else:
            resp_xml = ""
        self.write(resp_xml)

class QrcodeHandler(RequestHandler):
    """请求微信服务器生成带参数二维码返回"""
    @tornado.gen.coroutine
    def get(self):
        scene_id = self.get_argument("sid")
        try:
            access_token = yield AccessToken.get_access_token()
        except Exception as e:
            self.write("errmsg:%s"%e)
        else:
            client = AsyncHTTPClient()
            url = "https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s" % access_token
            req_data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            req = HTTPRequest(
                url = url,
                method = "POST",
                body = json.dumps(req_data)
            )
            resp = yield client.fetch(req)
            dict_data = json.loads(resp.body)
            if "errcode" in dict_data:
                self.write("errmsg:get qrcode failed")
            else:
                ticket = dict_data["ticket"]
                qrcode_url = dict_data["url"]
                self.write('<img src="https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket=%s"><br/>' % ticket)
                self.write('<p>%s</p>' % qrcode_url)

class ProfileHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument("code")
        client = AsyncHTTPClient()
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?" \
              "appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (WECHAT_APP_ID, WECHAT_APP_SECRET, code)
        resp = yield client.fetch(url)
        dict_data = json.loads(resp.body)
        if "errcode" in dict_data:
            self.write("error occur")
        else:
            access_token = dict_data["access_token"]
            open_id = dict_data["open_id"]
            url = "https://api.weixin.qq.com/sns/userinfo?" \
                  "access_token=%s&openid=%s&lang=zh_CN" % (access_token, open_id)
            resp = yield client.fetch(url)
            user_data = json.loads(resp.body)
            if "errcode" in user_data:
                self.write("error occur again")
            else:
                self.render("index.html", user = user_data)

# 获取图片素材列表(获取永久素材)
class GetmediaidHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            access_token = yield AccessToken.get_access_token()
        except Exception as e:
            self.write("errmsg:%s"%e)
        else:
            client = AsyncHTTPClient()
            # offset = self.get_argument('offset')
            # count = self.get_argument('count')
            url = "https://api.weixin.qq.com/cgi-bin/material/batchget_material?" \
                "access_token=%s" % access_token
            req_data = {"type":"image", "offset": 0, "count":15}
            req = HTTPRequest(
                url=url,
                method="POST",
                body = json.dumps(req_data, ensure_ascii=False).encode('gbk')
            )
            resp = yield client.fetch(req)
            dict_data = json.loads(resp.body)
            item = dict_data["item"]
            sqllist = []
            for i in range(0, len(item)):
                media_id = item[i]['media_id']
                media_url = item[i]['url']
                media_name = item[i]["name"]
                media_update_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(item[i]['update_time']))
                list = (media_id, media_url, media_name, media_update_time)
                sqllist.append(list)
            # 返回 图片ID,地址,图片名称,创建日期
            print(sqllist)

# 根据OpenID列表群发
class PosttextHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            access_token = yield AccessToken.get_access_token()
        except Exception as e:
            self.write("errmsg:%s"%e)
        else:
            client = AsyncHTTPClient()
            content = self.get_argument("content")
            a = int(time.time())
            url = "https://api.weixin.qq.com/cgi-bin/message/mass/send?access_token=%s" % access_token
            req_data = {"touser":["ouy9-jv31Y43nyYOfIfoYvBp_Wb8","ouy9-jv31Y43nyYOfIfoYvBp_Wb9"],
                        "msgtype": "text","text": { "content": content}, "clientmsgid":a }
            data = json.dumps(req_data, ensure_ascii=False).encode('utf-8')
            # a = requests.post(url, data=data)
            req = HTTPRequest(
                url=url,
                method="POST",
                body = json.dumps(req_data, ensure_ascii=False).encode('utf-8')
            )
            resp = yield client.fetch(req)
            dict_data = json.loads(resp.body)
            # 返回 错误代码errcode,错误信息errmsg,执行ID msg_id
            self.write('执行结果:%s' % dict_data['errmsg'])

# 提交永久图片
class SubmissionHandler(RequestHandler):
    @tornado.gen.coroutine
    def get(self):
        try:
            access_token = yield AccessToken.get_access_token()
            print(access_token)
        except Exception as e:
            self.write("errmsg:%s"%e)
        else:
            # type中可变图片（image）、语音（voice）、视频（video）和缩略图（thumb）
            url = "https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=%s&type=image" % access_token
            curl = 'C:\\curl\\curl\\bin\\curl.exe'
            dir = self.get_argument("dir")
            print(dir)
            # 'C:\\Users\\admin\\Desktop\\CCC.jpg'
            cmd = '%s -F media=@%s %s' % (curl, dir, url)
            os.system('chcp 65001')  # 更改GBK编码为UTF8编码
            a = os.popen(cmd)
            content = a.read()
            a.close()
            result = json.loads(content)
            if not result['errcode']:
                return [result['media_id'], result['url']]
            else:
                # return [result['errcode'], result['errmsg']]
                self.write(result['errmsg'])

def main():
    tornado.options.parse_command_line() # 转换命令行参数
    app = tornado.web.Application(
        [
            (r"/wechat8080", WechatHandler),
            (r"/qrcode", QrcodeHandler),
            (r"/wechat8080/profile", ProfileHandler),
            (r"/getmediaid", GetmediaidHandler),
            (r"/posttext", PosttextHandler),
            (r"/submission", SubmissionHandler)
        ],
        template_path = os.path.join(os.path.dirname(__file__), "template")
    )
    http_server = tornado.httpserver.HTTPServer(app) # 设置服务
    http_server.listen(options.port) # 设置监听
    tornado.ioloop.IOLoop.current().start() # 开启服务

if __name__== "__main__":
    main()
# https://api.weixin.qq.com/cgi-bin/user/get?access_token=27_uU_Fgr8jaRu76CqcUcwds_Sh3sp98azEoCiJ6cPGKXpLVIuRA2WgecHxUxpmNWDfKvQUndHWQPeXKN90Jv4bncEF9DgTDxj73nn5x2-qY9EUVtTakHzFq3OiA_3PV3q7z713HTMZ6_E70PmuIAObACAOGU