from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import requests, json

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# Replace these with your credentials
# LINE_ACCESS_TOKEN = "YOUR_CHANNEL_ACCESS_TOKEN"
# LINE_CHANNEL_SECRET = "YOUR_CHANNEL_SECRET"

app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    print(body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id  # Get User ID
    user_message = event.message.text

    reply = f"Your UID: {user_id}\nYou said: {user_message}"
    print(reply)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_message = event.message.text
#     reply = f"You said: {user_message}"
#     print(reply)
#     # line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

if __name__ == "__main__":
    app.run(port=5000)