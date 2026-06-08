import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, FlexSendMessage

app = Flask(__name__)

# 從環境變數讀取金鑰，請務必在部署平台上設定這些變數
line_bot_api = LineBotApi(os.environ.get('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.environ.get('CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_text = event.message.text.strip()
    
    # 觸發條件：只有當用戶輸入 "Hi" (不分大小寫) 時才觸發
    if user_text.lower() == "hi":
        flex_content = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {"type": "text", "text": "請問您在哪裡認識 Oldmoon 的呢?"},
                    {"type": "button", "action": {"type": "message", "label": "公園", "text": "公園"}},
                    {"type": "button", "action": {"type": "message", "label": "學校", "text": "學校"}},
                    {"type": "button", "action": {"type": "message", "label": "工作場合", "text": "工作場合"}},
                    {"type": "button", "action": {"type": "message", "label": "競賽", "text": "競賽"}},
                    {"type": "button", "action": {"type": "message", "label": "學術研討", "text": "學術研討"}}
                ]
            }
        }
        message = FlexSendMessage(alt_text="請選擇認識管道", contents=flex_content)
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    app.run()