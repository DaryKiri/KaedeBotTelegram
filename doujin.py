from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.error import TelegramError
from BotException import BotException
from nhentai import Nhentai

#TEST TODO
def send_error(bot, update, error_msg):
    """ Forcelly sends an error message """
    success = False
    while(not success):
        try:
            bot.send_message(chat_id=update.message.chat_id, text=error_msg)
            success = True
        except TelegramError:
            success = False

# TODO MAKE A CONVERSATION TYPE RESPONSE
# https://github.com/python-telegram-bot/python-telegram-bot/tree/0507378509257156abb6f2c550371eafa91556be/examples

class Doujin:
    def __init__(self, logger):
        self.hentai = Nhentai()
        self.logger = logger

    def doujin(self, bot, update, args):
        """ Post a random gallery, used for the python api command handler """
        chat_id = update.message.chat_id
        valid = False
        while(not valid):
            gallery = self.hentai.get_random_gallery()
            """
            if(chat_id < 0 and gallery.page_count <= 30):
                valid = True
            elif (chat_id > 0):
                valid = True
            """
            valid = True # Quitar despues
        
        images = gallery.images
        page = 1
        for image in images:
            try:
                bot.send_photo(chat_id=chat_id, photo=image.url, caption="Title: {0}\nPage: {1}/{2}\nSource: {3}".format(gallery.title, page, len(images), gallery.url))
                page = page + 1
            except TelegramError as e:
                self.logger.warn('Update "%s" caused error "%s"' % (update, e))
                send_error(bot,update,"Couldn't send image :<")
                #bot.send_message(chat_id=update.message.chat_id, text="Couldn't send image :<")