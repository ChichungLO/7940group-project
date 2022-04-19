#chatbot_test.py
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import configparser
import logging

import mysql.connector

global cnx

def main():
    # Load your token and create an Updater for your Bot
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global cnx
    cnx = mysql.connector.connect(user='comp7940gp13', password='comp7940gp13',
                              host='106.52.171.168',
                              database='comp7940gp13')

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler('cook', cook))
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    dispatcher.add_handler(CallbackQueryHandler(first_submenu1,
                                                pattern='m1_1'))
    dispatcher.add_handler(CallbackQueryHandler(second_submenu1,
                                                pattern='m2_1'))
    dispatcher.add_handler(CallbackQueryHandler(first_submenu2,
                                                pattern='m1_2'))
    dispatcher.add_handler(CallbackQueryHandler(second_submenu2,
                                                pattern='m2_2'))

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text= reply_message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Helping you helping you.')


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try: 
        global redis1
        logging.info(context.args[0])
        msg = context.args[0]   # /add keyword <-- this should store the keyword
        redis1.incr(msg)
        update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')

def cook(update, context):
    update.message.reply_text(main_menu_message(),
                            reply_markup=main_menu_keyboard())

def main_menu(update,context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=main_menu_message(),
                            reply_markup=main_menu_keyboard())

def first_menu(update,context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=first_menu_message(),
                            reply_markup=first_menu_keyboard())

def second_menu(update,context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=second_menu_message(),
                            reply_markup=second_menu_keyboard())

def first_submenu1(bot, update):
    update.message.reply_text('You choose first submenu1')

def first_submenu2(bot, update):
    update.message.reply_text('You choose first submenu2')

def second_submenu1(bot, update):
    update.message.reply_text('You choose second submenu1')

def second_submenu2(bot, update):
    update.message.reply_text('You choose second submenu2')

def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Chinese food', callback_data='m1')],
              [InlineKeyboardButton('Western food', callback_data='m2')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Tomato egg', callback_data='m1_1')],
              [InlineKeyboardButton('potato egg', callback_data='m1_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('fried chips', callback_data='m2_1')],
              [InlineKeyboardButton('hamburger', callback_data='m2_2')],
              [InlineKeyboardButton('Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def main_menu_message():
  return 'Choose the option in main menu:'

def first_menu_message():
  return 'Choose the food in Chinese food menu:'

def second_menu_message():
  return 'Choose the food in Western food menu:'


if __name__ == '__main__':
    main()