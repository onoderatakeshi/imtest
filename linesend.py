from flask import request, make_response
from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

access_token = ''

def line_send(user_id, msg):
    try:
        line_bot_api = LineBotApi(access_token)
        line_bot_api.push_message(user_id, TextSendMessage(text=msg))
    except LineBotApiError as e:
        print("api-error!")


def message_process(m_user_id, m_message_text):
    if m_message_text == 'whoami':
        message = str(m_user_id)
    elif m_message_text == 'Whoami':
        message = str(m_user_id)
    elif m_message_text == 'w':
        message = str(m_user_id)
    elif m_message_text == 'W':
        message = str(m_user_id)
    else:
        message = 'unknown'

    line_send(m_user_id, message)


def follow_process(m_user_id):
    message = str(m_user_id)
    line_send(m_user_id, message)

def parser(req_json):
    type = req_json['events'][0]['type']
    print("type = ", type)
    
    if type == "follow":
        m_timestamp = req_json['events'][0]['timestamp']
        m_replytoken = req_json['events'][0]['replyToken']
        
        m_user_type = req_json['events'][0]['source']['type']
        m_user_id = req_json['events'][0]['source']['userId']
        print("follow", m_timestamp, m_replytoken, m_user_type, m_user_id)
        follow_process(m_user_id)
        return 0
    elif type == "unfollow":
        m_timestamp = req_json['events'][0]['timestamp']
        m_replytoken = req_json['events'][0]['replyToken']
        
        m_user_type = req_json['events'][0]['source']['type']
        m_user_id = req_json['events'][0]['source']['userId']
        print("unfollow", m_timestamp, m_replytoken, m_user_type, m_user_id)
        return 1
    elif type == "message":
        m_timestamp = req_json['events'][0]['timestamp']
        m_replytoken = req_json['events'][0]['replyToken']
        
        m_user_type = req_json['events'][0]['source']['type']
        m_user_id = req_json['events'][0]['source']['userId']
        
        m_message_type = req_json['events'][0]['message']['type']
        m_message_id = req_json['events'][0]['message']['id']
        m_message_text = req_json['events'][0]['message']['text']
        print("message", m_timestamp, m_replytoken, m_user_type, m_user_id, m_message_type, m_message_id, m_message_text)

        message_process(m_user_id, m_message_text)
        return 2

def kakunin(request):
    try:
        req_json = request.get_json()
        parser(req_json)
    except Exception:
        resp = make_response("invalid param", 400)
        return resp
