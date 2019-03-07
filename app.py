from flask import Flask, request
import antolib
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError,
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)

line_bot_api = LineBotApi('/mO2Je84uD9n1o8Vz2qcxDQf8W/hFDykYbDP4q+59dIJ0QDc3+Jr4YUH+LEwzB8wQJtNvUsIFLXF+YX84g9E9rMYbx6R+c7FjP940fRuxYKV7gq0nWpEpbLThjAncEaILZ6eBlJUCQ2JH+/10bmo2wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('49b0435fe1a54671eebf49671eb0a273')

app = Flask(__name__)

# username of anto.io account
user = 'thanawatboonkear2@gmail.com'
# key of permission, generated on control panel anto.io
key = 'QSkbjOxbcOgFp7QJvDkfLxKXvHHv6NwI11HyGswl'
# your default thing.
thing = 'myDevice'

anto = antolib.Anto(user, key, thing)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    if(message == 'channel1 on'):
        anto.pub('myChannel1', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On channel1"))
    elif(message == 'channel1 off'):
        anto.pub('myChannel1', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel1"))
    elif(message == 'channel2 on'):
        anto.pub('myChannel2', 1)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn On channel2"))
    elif(message == 'channel2 off'):
        anto.pub('myChannel2', 0)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Turn Off channel2"))
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text="Turn Off channel1"))

if __name__ == "__main__":
    anto.mqtt.connect()
    app.run(debug=True)
