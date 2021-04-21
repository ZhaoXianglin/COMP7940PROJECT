import configparser
import logging
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext
from kkbox_developer_sdk.auth_flow import KKBOXOAuth
from kkbox_developer_sdk.api import KKBOXAPI
import random
import urllib
import requests

# 载入配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# 主程序
def run():

    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # 处理欢迎请求,/start触发
    dispatcher.add_handler(CommandHandler('start', welcome))
    # 处理所有文字请求
    text_handler = MessageHandler(Filters.text & (~Filters.command), nlp)
    dispatcher.add_handler(text_handler)
    # 处理地理位置请求
    location_handler = MessageHandler(Filters.location, returnlocation)
    dispatcher.add_handler(location_handler)
    # 处理图片卡路里计算
    cal_handler = MessageHandler(Filters.photo, image_handler)
    dispatcher.add_handler(cal_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()


# 打卡成功
def returnlocation(bot, update):
    key = config['MAP']['KEY']
    url = 'https://restapi.amap.com/v3/geocode/regeo'
    params = {
        "location": str(bot.message['location']['longitude'])+','+str(bot.message['location']['latitude']),
        "output": 'json',
        "key": key,
    }
    r = requests.get(url=url, params=params)
    add = r.json()['formatted_address']
    replay_message = "打卡成功！"
    update.bot.send_message(chat_id=bot.effective_chat.id, text=replay_message)


# 欢迎信息
def welcome(update, context):
    welcome_message = '''欢迎使用运动助手机器人,您可以这样和我说
                        - 帮我计算我的BMI 
                        - 我在运动，给我来点音乐 
                        - 给我发张实物图片，帮你计算食物卡路里 
                        - 给我瑜伽的运动指导 
                        - 户外运动打卡 
                        也可以试着和我闲聊，比如今天天气如何？
    '''
    reply_keyboard_markup = ReplyKeyboardMarkup([['香港今天天气如何'], ['给我讲个笑话吧'], ['你好吗'], ['给我来点运动时听的音乐'], ['瑜伽要怎么做']])
    user = update.message.from_user
    print('You talk with user {} and his user ID: {} '.format(user['username'], user['id']))
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, reply_markup=reply_keyboard_markup)


# 所有的文字信息转发dialogflow处理
def nlp(update, context):
    msg_text = update.message.text
    intent, res_text = detect_intent_texts("comp7930-final-ipxa", '123456789', msg_text, 'zh-CN')
    print(intent, '---')
    if intent == 'music':
        print("在这")
        auth = KKBOXOAuth(config['KKBOX']['ID'], config['KKBOX']['SECRET'])
        token = auth.fetch_access_token_by_client_credentials()
        kkboxapi = KKBOXAPI(token)
        search_results = kkboxapi.search_fetcher.search('workout', types=['playlist'], terr='HK')
        playlists = search_results['playlists']['data']
        rdmnumber = random.randint(0, len(playlists)-1)
        first = playlists[rdmnumber]
        print(first)
        context.bot.send_message(chat_id=update.effective_chat.id, text=first['title'])
        context.bot.send_photo(chat_id=update.effective_chat.id,photo=first['images'][0]["url"])
        context.bot.send_message(chat_id=update.effective_chat.id, text=first['url'])
    elif intent == 'Default Fallback Intent':
        # 找不到意图的，就转发给机器人处理
        url = 'http://api.qingyunke.com/api.php?key=free&appid=0&msg={}'.format(urllib.parse.quote(msg_text))
        res = requests.get(url)
        context.bot.send_message(chat_id=update.effective_chat.id, text=res.json()["content"])

    elif intent == 'card':
        # 调用打卡意图
        reply_markup = ReplyKeyboardMarkup(
            [[KeyboardButton('共享位置', request_location=True)]],
            resize_keyboard=True,
            one_time_keyboard=True,
        )
        message = "请共享你的打卡位置"
        context.bot.send_message(chat_id=update.message.chat_id, text=message, reply_markup=reply_markup)
    else:
        # print("hellwo")
        context.bot.send_message(chat_id=update.effective_chat.id, text=res_text)


def image_handler(bot, update):
    file = bot.message.photo[-1].file_id
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    file = updater.bot.get_file(file)
    file.download()
    print(file, type(update), type(bot))
    print(bot.message.photo[-1])


def detect_intent_texts(project_id, session_id, text, language_code):
    """检测输入返回意图名称"""
    from google.cloud import dialogflow
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input})
    # 意图和置信度
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    # 返回的答案
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text))
    return response.query_result.intent.display_name, response.query_result.fulfillment_text


if __name__ == '__main__':
    run()
