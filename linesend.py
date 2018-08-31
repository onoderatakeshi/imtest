from flask import request, make_response
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

access_token = ''


class LineString:
    def __init__(self, req_json):
        self.req_json = req_json
        self.message_type = req_json['events'][0]['type']
        self.timestamp    = req_json['events'][0]['timestamp']
        self.replytoken   = ""

    def parse(self):
        if self.message_type == "follow":
            self.replytoken = self.req_json['events'][0]['replyToken']
            m_user_type     = self.req_json['events'][0]['source']['type']
            m_user_id       = self.req_json['events'][0]['source']['userId']
            print("ls:follow", self.timestamp, self.replytoken, m_user_type, m_user_id)
            self.follow_process(m_user_id)
            return "follow"
            
        elif self.message_type == "unfollow":
            m_user_type = self.req_json['events'][0]['source']['type']
            m_user_id   = self.req_json['events'][0]['source']['userId']
            print("ls:unfollow", self.timestamp, self.replytoken, m_user_type, m_user_id)
            return "unfollow"
            
        elif self.message_type == "message":
            self.replytoken = self.req_json['events'][0]['replyToken']
            m_user_type     = self.req_json['events'][0]['source']['type']
            m_user_id       = self.req_json['events'][0]['source']['userId']
            
            m_message_type  = self.req_json['events'][0]['message']['type']
            m_message_id    = self.req_json['events'][0]['message']['id']
            m_message_text  = self.req_json['events'][0]['message']['text']
            print("ls:message", self.timestamp, self.replytoken, m_user_type, m_user_id, m_message_type, m_message_id, m_message_text)
            self.message_process(m_user_id, m_message_text)
            return "message"
            
        else:
            print("ls:unknown")
            return "unknown"

    def output(self):
        print("message_type = ", self.message_type)
        print("timestamp = ", self.timestamp)
        print("replytoken = ", self.replytoken)

    def follow_process(self, m_user_id):
        message = str(m_user_id)
        line_send(m_user_id, message)

    def message_process(self, m_user_id, m_message_text):
        if m_message_text == 'whoami':
            message = str(m_user_id)
        elif m_message_text == 'Whoami':
            message = str(m_user_id)
        elif m_message_text == 'w':
            message = str(m_user_id)
        elif m_message_text == 'W':
            message = str(m_user_id)
        elif m_message_text == 'a':
            message = 'user_id = ' + str(m_user_id)
        else:
            message = 'unknown'
        
        line_send(m_user_id, message)


def line_send(user_id, msg):
    try:
        line_bot_api = LineBotApi(access_token)
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
    except LineBotApiError as e:
        print("api-error!")


def kakunin(request):
    print(request.args)
        
    try:
        req_json = request.get_json()
        ls = LineString(req_json)
        ls.parse()
        
    except Exception:
        resp = make_response("invalid param", 400)
        return resp
