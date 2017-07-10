#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TODO
    - Add documentation
    - Sankaku complex support
    - Safebooru support
    - Conversation support with kaede quotes (pastebin???)
    - CLEAN MAIN
    - Popular images (?)
    - Sticker support (?)
    - Statistics and logging
    - Put worker on heroku
    - Lewd photos support from danbooru
    - Pixiv support
    - Comands: /latest, /random, /card, /video, /lewd
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove, ParseMode)
from telegram.error import TelegramError
from BotException import BotException
from doujin import Doujin
import random as rnd_gen
import logging
import requester
import re
import os
import voices
import imgur
import youtube

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

reply_keyboard = [['/latest', '/random', '/voice'], ['/card', '/video', '/doujin'], ['/help']]

admin_id = [302205207]

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    update.message.reply_text("I'm Kaede Takagaki, take care of me, Producer.",
    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

def help(bot, update):
    help_text = """ 
I'm a bot that replies images and videos from Kaede Takagaki

<b>Commands</b>
/start - Starts the bot
/help - Prints again this help message
/latest - [imageboard] [number] Gets a [number] of latest images from a [imageboard]
/random - [imageboard] [number] Gets a [number] of random images from a [imageboard] 
/voice - Sends a [type] of voice clip
/card - Sends a [number] of official Kaede cards
/video - Sends a [number] of random videos from youtube 
    """
    bot.send_message(chat_id=update.message.chat_id,text=help_text,
                    parse_mode=ParseMode.HTML)
    #update.message.reply_text(help_text)

def echo(bot, update):
    print(update.message.from_user.id)
    pass
    #print(update.message.message_id)
    #update.message.reply_text(update.message.text)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))  

def latest(bot, update, args):
    if(args):
        if(not args[0] in requester.imgboards):
            update.message.reply_text("Valid imageboards: {0}".format(requester.imgboards))
            return
        else:
            board = args[0]
    else:
        board = rnd_gen.randrange(len(requester.imgboards))

    if(len(args) > 1): 
        try:
            result_count = int(args[1])
            if(result_count > 5 and update.message.chat_id < 0 and not update.message.from_user.id in admin_id):
                raise RuntimeError()

            result = requester.get_image_batch(imageboard=board, random=False, result_count=result_count)
            for image in result:
                try:
                    bot.send_photo(chat_id=update.message.chat_id, photo=image['url'], caption=image['caption'])
                except TelegramError:
                    logger.warn('Update "%s" caused error "%s"' % (update, error))
                    bot.send_message(chat_id=update.message.chat_id, text="Couldn't send image :<")
        
        except ValueError:
            update.message.reply_text('Command format: /latest [imageboard] [number]')
        except RuntimeError:
            update.message.reply_text('You can only send 5 images on group chats')
    else:
        try:
            result = requester.get_image(imageboard=board, random=False)
            bot.send_photo(chat_id=update.message.chat_id, photo=result['url'], caption=result['caption'])
        except TelegramError:
            logger.warn('Update "%s" caused error "%s"' % (update, error))
            bot.send_message(chat_id=update.message.chat_id, text="Couldn't send image :<")

def random_img(bot, update, args):
    if(args):
        if(not args[0] in requester.imgboards):
            update.message.reply_text("Valid imageboards: {0}".format(requester.imgboards))
            return
        else:
            board = args[0]
    else:
        board = rnd_gen.randrange(len(requester.imgboards))

    if(len(args) > 1): 
        try:
            result_count = int(args[1])
            if(result_count > 5 and update.message.chat_id < 0 and not update.message.from_user.id in admin_id):
                raise RuntimeError()

            result = requester.get_image_batch(imageboard=board, random=True, result_count=result_count)
            for image in result:
                try:
                    bot.send_photo(chat_id=update.message.chat_id, photo=image['url'], caption=image['caption'])
                except TelegramError:
                    logger.warn('Update "%s" caused error "%s"' % (update, error))
                    bot.send_message(chat_id=update.message.chat_id, text="Couldn't send image :<")

        except ValueError:
            update.message.reply_text('Command format: /random [imageboard] [number]')
        except RuntimeError:
            update.message.reply_text('You can only send 5 images on group chats')
    else:
        result = requester.get_image(imageboard=board, random=True)
        bot.send_photo(chat_id=update.message.chat_id, photo=result['url'], caption=result['caption'])
    
def voice(bot, update, args):
    try:
        if(args):
            file_path = voices.get_voice(type_voice=args[0])
        else:
            file_path = voices.get_voice(type_voice='random')

        bot.send_voice(chat_id=update.message.chat_id,voice=open(file_path, 'rb'))
    except TelegramError:
        logger.warn('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id, text="Couldn't send voiceclip :<")
    except RuntimeError as e:
        update.message.reply_text("{0}".format(str(e)))

def card(bot, update, args):
    try:
        if(args):
            count = int(args[0])

            if(count > 5 and update.message.chat_id < 0 and not update.message.from_user.id in admin_id):
                raise BotException 

            url_image = imgur.get_random_card(count=count)
        else:
            url_image = imgur.get_random_card()
        
        for url in url_image:
            bot.send_photo(chat_id=update.message.chat_id, photo=url)

    except TelegramError:
        logger.warn('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id, text="Couldn't send a random card :<")
    except RuntimeError as e:
        logger.warn('Error "%s"' % (str(e)))
        bot.send_message(chat_id=update.message.chat_id, text="Couldn't send a random card :<")
    except ValueError:
        update.message.reply_text("Command format: /card [number]")
    except BotException:
        bot.send_message(chat_id=update.message.chat_id, text="You can only send 5 cards on group chats")

def video(bot, update, args):
    try:
        if(args):
            result_count = int(args[0])
            
            if(result_count > 5 and update.message.chat_id < 0 and not update.message.from_user.id in admin_id):
                raise BotException 

            #Handle multiple pages and count of videos
            num_videos = 0
            has_next_page = True
            page = None
            videos = []
            while (has_next_page and num_videos < result_count):
                res = youtube.get_video(page=page)

                #  Save source videos on video list
                i = 0
                while(i < res['totalResults'] and num_videos < result_count):
                    videos.append(res['sources'][i])
                    i = i + 1
                    num_videos = num_videos + 1

                if(res['nextPageToken']):
                    page = res['nextPageToken']
                else:
                    page = None
                    has_next_page = False
            
        else:
            res = youtube.get_video()
            videos = res['sources'][0:1]

        # Send the videos
        for video in videos:
            try:
                #print(video)
                bot.send_message(chat_id=update.message.chat_id, text=video)
            except TelegramError:
                logger.warn('Update "%s" caused error "%s"' % (update, error))
                bot.send_message(chat_id=update.message.chat_id, text="Couldn't send a video :<")

    except TelegramError:
        logger.warn('Update "%s" caused error "%s"' % (update, error))
        bot.send_message(chat_id=update.message.chat_id, text="Couldn't send a video :<")
    except ValueError:
        update.message.reply_text("Command format: /video [number]")
    except BotException:
        bot.send_message(chat_id=update.message.chat_id, text="You can only send 5 videos on group chats")


def main():
    # Create Doujin handler
    doujin_handler = Doujin(logger)

    # Create the EventHandler and pass it your bot's token.
    updater = Updater("")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler(command="random", callback=random_img, pass_args=True))
    dp.add_handler(CommandHandler(command="latest", callback=latest, pass_args=True))
    dp.add_handler(CommandHandler(command="voice", callback=voice, pass_args=True))
    dp.add_handler(CommandHandler(command="card", callback=card, pass_args=True))
    dp.add_handler(CommandHandler(command="video", callback=video, pass_args=True))

    dp.add_handler(CommandHandler(command="doujin", callback=doujin_handler.doujin, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    #dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    print("going to idle")
    updater.idle()


if __name__ == '__main__':
    print("starting")
    main()