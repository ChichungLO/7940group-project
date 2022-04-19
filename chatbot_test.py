#chatbot_test.py
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import configparser
import logging

import psycopg2

global cnx
global cur

def main():
    # Load your token and create an Updater for your Bot
    
    config = configparser.ConfigParser()
    config.read('config.ini')
    updater = Updater(token=(config['TELEGRAM']['ACCESS_TOKEN']), use_context=True)
    dispatcher = updater.dispatcher

    global cnx
    cnx = psycopg2.connect(host="ec2-44-194-4-127.compute-1.amazonaws.com", 
                user="kouyhyskzsssia", 
                dbname="d9meetj91bb2ms",
                password="f21744c8bfe917ea276c6b044fcf0362e50920f32143a927489d076b6d44493a", 
                sslmode='require')
    global cur 
    cur = cnx.cursor()

    # You can set this logging module, so you will know when and why things do not work as expected
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    
    # register a dispatcher to handle message: here we register an echo dispatcher
    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(echo_handler)

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    #dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(CommandHandler('cook', cook))
    dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    dispatcher.add_handler(CallbackQueryHandler(first_menu, pattern='m1'))
    dispatcher.add_handler(CallbackQueryHandler(second_menu, pattern='m2'))
    dispatcher.add_handler(CallbackQueryHandler(first_submenu1,
                                                pattern='fm1'))
    dispatcher.add_handler(CallbackQueryHandler(second_submenu1,
                                                pattern='sm1'))
    dispatcher.add_handler(CallbackQueryHandler(first_submenu2,
                                                pattern='fm2'))
    dispatcher.add_handler(CallbackQueryHandler(second_submenu2,
                                                pattern='sm2'))
    #cook video click times stats
    dispatcher.add_handler(CommandHandler('stat', cook_stat))

    # To start the bot:
    updater.start_polling()
    updater.idle()



def echo(update, context):
    update.message.reply_text(
        "If you want to use command, try /help to see which command you like!")


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "This is a cooking video recommendation robot! \nType /cook to see which food you like!")

def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('To see the cook video menu:\n /cook\n\nTo see the most popular cook video:\n /stat')



# def add(update: Update, context: CallbackContext) -> None:
#     """Send a message when the command /add is issued."""
#     try: 
#         global redis1
#         logging.info(context.args[0])
#         msg = context.args[0]   # /add keyword <-- this should store the keyword
#         redis1.incr(msg)
#         update.message.reply_text('You have said ' + msg +  ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
#     except (IndexError, ValueError):
#         update.message.reply_text('Usage: /add <keyword>')

def cook_stat(update, context):
    global cur, cnx
    cur.execute("SELECT NAME, TIMES FROM COOK WHERE TIMES = (SELECT MAX(TIMES) FROM COOK)")
    rows = cur.fetchall()
    for row in rows:
        if row[0] == 'tomato':
            update.message.reply_text('The most popular cooking video is Fried eggs with Tomato! \n【' + str(row[1]) + '】 clicks in total.')
        elif row[0] == 'tofu':
            update.message.reply_text('The most popular cooking video is Mapo Tofu! \n【' + str(row[1]) + '】 clicks in total.')
        elif row[0] == 'chips':
            update.message.reply_text('The most popular cooking video is Fish and Chips! \n【' + str(row[1]) + '】 clicks in total.')
        else:
            update.message.reply_text('The most popular cooking video is Hamburger! \n【' + str(row[1]) + '】 clicks in total.')


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
    query = bot.callback_query
    query.answer()
    query.edit_message_text(text=first_submenu1_message(),
                            reply_markup=return_menu_keyboard())
    global cur, cnx
    cur.execute("UPDATE COOK SET TIMES = TIMES+1 WHERE name='tomato'")
    cnx.commit()

def first_submenu2(bot, update):
    query = bot.callback_query
    query.answer()
    query.edit_message_text(text=first_submenu2_message(),
                            reply_markup=return_menu_keyboard())
    global cur, cnx
    cur.execute("UPDATE COOK SET TIMES = TIMES+1 WHERE name='tofu'")
    cnx.commit()

def second_submenu1(bot, update):
    query = bot.callback_query
    query.answer()
    query.edit_message_text(text=second_submenu1_message(),
                            reply_markup=return_menu_keyboard())
    global cur, cnx
    cur.execute("UPDATE COOK SET TIMES = TIMES+1 WHERE name='chips'")
    cnx.commit()

def second_submenu2(bot, update):
    query = bot.callback_query
    query.answer()
    query.edit_message_text(text=second_submenu2_message(),
                            reply_markup=return_menu_keyboard())
    global cur, cnx
    cur.execute("UPDATE COOK SET TIMES = TIMES+1 WHERE name='burger'")
    cnx.commit()

def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Chinese food', callback_data='m1')],
              [InlineKeyboardButton('Western food', callback_data='m2')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Fried eggs with Tomato', callback_data='fm1')],
              [InlineKeyboardButton('Mapo Tofu', callback_data='fm2')],
              [InlineKeyboardButton('⬅️ Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Fish and Chips', callback_data='sm1')],
              [InlineKeyboardButton('Hamburger', callback_data='sm2')],
              [InlineKeyboardButton('⬅️ Main menuu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def return_menu_keyboard():
  keyboard = [[InlineKeyboardButton('⬅️ Main menu', callback_data='main')]]
  return InlineKeyboardMarkup(keyboard)

def main_menu_message():
  return 'Choose the option in main menu:'

def first_menu_message():
  return 'Choose the food in Chinese food menu:'

def second_menu_message():
  return 'Choose the food in Western food menu:'

def first_submenu1_message():
    return 'https://www.youtube.com/watch?v=2hvQFxZBTVY'

def first_submenu2_message():
    return 'https://www.youtube.com/watch?v=ZfsZwwrTFD4'

def second_submenu1_message():
    return 'https://www.youtube.com/watch?v=zit9l5jtbws'

def second_submenu2_message():
    return 'https://www.youtube.com/watch?v=iM_KMYulI_s'


if __name__ == '__main__':
    main()