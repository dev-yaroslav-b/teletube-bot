#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
import re
import time

from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from bot.helpers import download_audio_or_playlist, clean, recommend_song, handle_time_codes, split_file

base_dir = os.path.dirname(os.path.realpath(__file__))

# Setup logging
bot_log_filename = 'bot_logs.log'
logging.basicConfig(filename='bot/logs/{}'.format(bot_log_filename),
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    update.message.reply_text("""Hi! Let me show my commands - /help""")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""My commands:
    /send `your-youtube-url` - and I will send you audio file or even playlist;
    /recommend `artist-song` - and I will recommend you similar song(THIS PATTERN IS MUST);
    /podcast `your-youtube-url` `time codes` - and I will send you separated audio files;
    /help - in case you forgot something;
    """)


def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, context.error)


def send(update: Update, context: CallbackContext):
    data = {
        'url': re.sub('/\w+\s', '', update.message['text']),
        'chat_id': str(update.message.chat_id)
    }
    logging.info("Chat id: {} | Downloading {}".format(data['chat_id'], data['url']))
    audio_dir = base_dir + '/audio/' + data['chat_id']

    try:
        download_audio_or_playlist(audio_dir, data['url'])
        logging.info("Downloaded successfully")

        for filename in os.listdir(audio_dir):
            context.bot.send_audio(chat_id=data['chat_id'], audio=open(os.path.join(audio_dir, filename), 'rb'),
                                   timeout=1000)
            logging.info("Sent {} successfully".format(filename))

        logging.info("Deleting {}".format(audio_dir))
        logging.info(clean(audio_dir))

        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    except:
        logging.error("Exception occurred", exc_info=True)
        update.message.reply_text("Unknown error occurred! Please, try again later")


def podcast(update: Update, context: CallbackContext):
    data = {
        'url': re.sub('/\w+\s', '', update.message['text']),
        'time_codes': update.message['text'].split(' ')[2:],
        'chat_id': str(update.message.chat_id)
    }
    logging.info("Chat id: {} | Downloading {}".format(data['chat_id'], data['url']))
    audio_dir = base_dir + '/audio/' + data['chat_id']
    try:
        data['time_codes'] = handle_time_codes(' '.join(data['time_codes']))
        logging.info("Processed time codes successfully")

        download_audio_or_playlist(audio_dir, data['url'])
        logging.info("Downloaded successfully")

        filename_parts = split_file(data['time_codes'], audio_dir)
        logging.info("Split files successfully")

        for k, filename in filename_parts.items():
            context.bot.send_audio(chat_id=data['chat_id'], audio=open(os.path.join(audio_dir, filename), 'rb'),
                                   timeout=1000)
            logging.info("Sent {} successfully".format(filename))

        logging.info("Deleting {}".format(audio_dir))
        logging.info(clean(audio_dir))

        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
    except:
        logging.error("Exception occurred", exc_info=True)
        update.message.reply_text("Unknown error occurred! Please, try again later")


def recommend(update: Update, context: CallbackContext):
    data = {
        'info': re.sub('/\w+\s', '', update.message['text']),
        'chat_id': str(update.message.chat_id)
    }
    logging.info("Chat id: {} | Recommend request: {}".format(data['chat_id'], data['info']))

    artist, song = data['info'].split('-')
    logging.info("Searching for {} - {}".format(artist, song))

    recommendation = recommend_song(artist, song)
    logging.info("Searching result: {}".format(recommendation))

    if recommendation is None:
        update.message.reply_text("Can't find any similar songs :(")
    else:
        for s in recommendation:
            update.message.reply_text('{}: {}\n{}'.format(s[0], s[1], s[2]))


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(os.environ.get('TOKEN'), use_context=True)

    logging.info('I am alive')

    # Bot commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('send', send))
    updater.dispatcher.add_handler(CommandHandler('podcast', podcast))
    updater.dispatcher.add_handler(CommandHandler('recommend', recommend))

    # updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()
