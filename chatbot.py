import configparser
import logging
from baidu.AipImageClassify import calorie
from telegram.ext import Updater,Dispatcher, MessageHandler, Filters,CommandHandler,CallbackContext
import requests
import json
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
    dispatcher.add_handler(CommandHandler('hello',hello))
    dispatcher.add_handler(echo_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()

def hello(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


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
        replay_message="The calorie of this food is "+output['result'][0]['calorie'] +"KJ"   
        update.bot.send_message(chat_id=bot.effective_chat.id, text=replay_message)
    #print(output['result'][0]['calorie'])
    
   


if __name__ == '__main__':
    run()