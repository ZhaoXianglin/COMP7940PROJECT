import configparser
import logging

from telegram.ext import Updater,Dispatcher, MessageHandler, Filters,CommandHandler,CallbackContext

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
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    file = updater.bot.get_file(file)
    file.download()
    print(file,type(update),type(bot))
    print(bot.message.photo[-1])


if __name__ == '__main__':
    run()