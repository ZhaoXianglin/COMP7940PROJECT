import configparser
import logging
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext

# 载入配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def run():

    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher
    # 处理欢迎请求,/start触发
    dispatcher.add_handler(CommandHandler('start', welcome))
    # 处理所有文字请求
    text_handler = MessageHandler(Filters.text & (~Filters.command), nlp)
    dispatcher.add_handler(text_handler)

    # 处理图片卡路里计算
    cal_handler = MessageHandler(Filters.photo, image_handler)
    dispatcher.add_handler(cal_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()


def welcome(update, context):
    welcome_message = '''欢迎使用运动助手机器人,您可以这样和我说
                        - 帮我计算我的BMI 
                        - 我在运动，给我来点音乐 
                        - 给我发张实物图片，帮你计算食物卡路里 
                        - 给我瑜伽的运动指导 
                        - 户外运动打卡 
                        也可以试着和我闲聊，比如今天天气如何？
    '''
    reply_keyboard_markup = ReplyKeyboardMarkup([['香港今天天气如何'],['给我讲个笑話'],['你好吗'],['给我来点运动时听的音乐'],['瑜伽要怎么做']])

    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message, reply_markup = reply_keyboard_markup)


# 所有的文字信息转发dialogflow
def nlp(update, context):
    msg_text = update.message.text
    print(type(msg_text))
    res_text = detect_intent_texts("comp7930-final-ipxa", '123456789', msg_text, 'zh-CN')
    context.bot.send_message(chat_id=update.effective_chat.id, text=res_text)


def image_handler(bot, update):
    file = bot.message.photo[-1].file_id
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    file = updater.bot.get_file(file)
    file.download()
    print(file,type(update),type(bot))
    print(bot.message.photo[-1])


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
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
    return response.query_result.fulfillment_text


if __name__ == '__main__':
    run()
