#-- coding:UTF-8 --
import configparser
import logging
from api import calorie
from telegram.ext import Updater, MessageHandler, Filters,CommandHandler
from telegram import (ReplyKeyboardMarkup, KeyboardButton)
# 载入配置文件
config = configparser.ConfigParser()
config.read('config.ini')

# 日志
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
API_TOKEN=config['TELEGRAM']['ACCESS_TOKEN']

def run():

    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)

    dispatcher = updater.dispatcher
    echo_handler = MessageHandler(Filters.photo, image_handler)
    location_handler = MessageHandler(Filters.location, returnlocation)
    dispatcher.add_handler(CommandHandler('hello',hello))
    dispatcher.add_handler(echo_handler)
    dispatcher.add_handler(location_handler)
    dispatcher.add_handler(CommandHandler('location', location))
    # To start the bot:
    updater.start_polling()
    updater.idle()


def hello(bot, update):
    reply_message = bot.message.text.upper()
    # print(update)
    logging.info("Update: " + str(update))
    # logging.info("context: " + str(context))
    update.bot.send_message(chat_id=bot.effective_chat.id, text=reply_message)


def returnlocation(bot,update):
    replay_message = "打卡成功！"
    update.bot.send_message(chat_id=bot.effective_chat.id, text=replay_message)


    print("打卡成功！")
def location(bot, update):
    reply_markup = ReplyKeyboardMarkup(
        [[KeyboardButton('共享位置', request_location=True)]],
        resize_keyboard= True,
        one_time_keyboard=True,
    )
    message = "请共享你的打卡位置"
    update.bot.send_message(chat_id=bot.message.chat_id, text=message, reply_markup=reply_markup)


def image_handler(bot, update):
    file = bot.message.photo[-1].file_id
    #print(type(FileExistsError))

    #ile_info=requests.get('https://api.telegram.org/bot{0}/getFile?file_id={1}'.format(API_TOKEN, file_info))
    #file_info=file_info.file_path
    #file_dict = json.load(file_info)
    #print(file_info.file_path)
    #file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, file_info.file_path))
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    file = updater.bot.get_file(file)
    file.download("1.jpg")
    with open("1.jpg",'rb') as photo:
        output=calorie(photo.read())
    #calorie("1.jpg")
    print(output)

    if str(output['result'][0]['has_calorie'])=='False':

        update.bot.send_message(chat_id=bot.effective_chat.id, text="Can not recognize any food in the image")
    else:
        replay_message="The calorie of this food is "+output['result'][0]['calorie'] +" kj"
        update.bot.send_message(chat_id=bot.effective_chat.id, text=replay_message)
    #print(output['result'][0]['calorie'])


if __name__ == '__main__':
    run()
