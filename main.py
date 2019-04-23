import telegram
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram.ext import ConversationHandler

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

file = 'AnelyaBot-5f745e570dca.json'
creds = ServiceAccountCredentials.from_json_keyfile_name(file,scope)
client = gspread.authorize(creds)

url = 'https://docs.google.com/spreadsheets/d/1nYsrePTTlH3ODVfkx08jNmBkChXmMZDNht1lNn18dNA/edit?usp=sharing'
sheet = client.open_by_url(url).sheet1

token= '644918890:AAGK1WHQHCuLoxi9Hq1Jpb4gn0zjiu7iDQI'

def start(update, context):
  text=update.message.text
  chat_id = update.message.chat_id

  print(f"text:{text}")
  print (f"chat_id: {chat_id}")
  context.bot.send_message(chat_id=chat_id,
    text="Hello! My name is AnelyaBeauty and i want to deliver you happiness today!\n press /help to get to know me \n press /prefer to start your order")

def help(update, context):
  text=update.message.text
  chat_id = update.message.chat_id

  print(f"text:{text}")
  print (f"chat_id: {chat_id}")
  context.bot.send_message(chat_id=chat_id,
    text="This is the Telegram Bot for AnelyaBeauty.\nWelcome to the world of cosmetics and perfumes <3\nHow Can I Help You Today?")

def prefer (update, context):
  text=update.message.text
  chat_id = update.message.chat_id

  print(f"text:{text}")
  print (f"chat_id: {chat_id}")
 
  custom_keyboard = [['cosmetics', 'perfume']]
  reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)

  context.bot.send_message(chat_id=chat_id, 
    text="What do You Prefer today?", 
    reply_markup=reply_markup)
  return 1

def first (update, context):
  chat_id=update.message.chat_id
  text=update.message.text

  user_data=context.user_data
  user_data['type'] = text
  user_data['first_name'] = update.message.chat.first_name
  user_data['last_name']= update.message.chat.last_name
  user_data['username'] = update.message.chat.username


  context.bot.send_message(chat_id=chat_id,
    text="Give me the name of the item please")
  return 2

def second (update, context):
  chat_id= update.message.chat_id
  text= update.message.text

  user_data= context.user_data
  user_data['item']=text

  context.bot.send_message(chat_id=chat_id,
    text='Give me your address please')
  return 3

def third (update, context):
  chat_id=update.message.chat_id
  text=update.message.text

  user_data=context.user_data
  user_data['address']=text

  to_add=[user_data['first_name'],user_data['last_name'], user_data['username'], user_data['type'], user_data['item'],user_data['address']]
  sheet.insert_row(to_add)

  context.bot.send_message(chat_id=chat_id,
    text='Thank You for Your Order and Have a Great Day! :)')
  print(user_data)
  return ConversationHandler.END

def cancel(update, context):
  chat_id = update.message.chat_id
  text = update.message.text

  context.bot.send_message(chat_id=chat_id,
    text='You have cancelled the order. To start again please command /prefer ')
  return ConversationHandler.END


def admin(update, context):
  chat_id=update.message.chat_id
  context.bot.send_message(chat_id=chat_id, text= f'{a.Type} {a.Item} {a.Address}')

upd = Updater(token, use_context=True)

start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', help)

admin_handler = CommandHandler('admin', admin)


dialog_handler = ConversationHandler(
  entry_points=[CommandHandler('prefer', prefer)],
  states={
    1: [MessageHandler(Filters.text, first, pass_user_data=True)],
    2: [MessageHandler(Filters.text, second, pass_user_data=True)],
    3: [MessageHandler(Filters.text, third, pass_user_data=True)]
  },
  fallbacks=[CommandHandler('cancel', cancel, pass_user_data=True)]
)



dispatcher = upd.dispatcher
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(admin_handler)
dispatcher.add_handler(dialog_handler)

upd.start_polling()
upd.idle()
