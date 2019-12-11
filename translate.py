import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters 
import googletrans
from googletrans import Translator

translator = Translator()

user_preference = {}

all_lang = googletrans.LANGUAGES
langcodes = dict(map(reversed,all_lang.items()))

def start(update, context):
  message = "WELCOME " + update.message.from_user.first_name
  context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def check_lang(update,context):
  user = update.message.from_user.username
  try:
    send_message = "Current language is set to " + user_preference[user].upper()
    context.bot.send_message(chat_id = update.effective_chat.id, text = send_message)
  except:
    send_message = "No language has been set yet"
    context.bot.send_message(chat_id = update.effective_chat.id, text = send_message)

def set_preferences(update,context):
  user = update.message.from_user.username
  msg = update.message.text
  msg = msg[5:].strip()
  msg = msg.lower()
  if len(msg) == 0:
    context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
  elif msg not in langcodes.keys():
    context.bot.send_message(chat_id=update.effective_chat.id, text = "Language code not supported by Google Translate")
  else:
    try:
      user_preference[user] = msg
    except:
      user_preference[user] = msg
    text_message = str(msg.upper()) + " set for " + update.message.from_user.first_name
    context.bot.send_message(chat_id=update.effective_chat.id, text = text_message)

def translate(update,context):
  user = update.message.from_user.username
  try:
    translation_language = user_preference[user]
  except:
    context.bot.send_message(chat_id=update.effective_chat.id, text = "You have not set a language for translation")
    return
  msg = update.message.text
  msg = msg[10:]
  if len(msg) == 0:
    context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
  else:
    msg = msg.strip().lower()
    translated = translator.translate(msg,dest = translation_language)
    send_message = "TRANSLATED TEXT: " + str(translated.text)
    context.bot.send_message(chat_id=update.effective_chat.id, text = send_message)

def unknown(update, context):
  context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

def check_language(update,context):

    msg = update.message.text
    msg = msg[6:]
    if len(msg) == 0:
      context.bot.send_message(chat_id = update.effective_chat.id, text = "No valid placeholders. Please run the command again!!")
    else:
      msg = msg.strip()
      language = translator.detect(msg)
      lang_text = all_lang[language.lang.lower()]
      send_message = "Detected language: " + str(lang_text.upper()) + " Confidence: " + str(language.confidence)
      context.bot.send_message(chat_id = update.effective_chat.id, text = send_message)

def main():
  bot = telegram.Bot(token=<token>)
  updater = Updater(token=<token>, use_context = True)
  dispatcher = updater.dispatcher
  print('bot started')
  dispatcher.add_handler(CommandHandler("start", start, pass_args = True))
  dispatcher.add_handler(CommandHandler("translate", translate, pass_args = True))
  dispatcher.add_handler(CommandHandler("check", check_language, pass_args = True))
  dispatcher.add_handler(CommandHandler("lang", set_preferences, pass_args = True))
  dispatcher.add_handler(CommandHandler("checklang", check_lang, pass_args = True))
  dispatcher.add_handler(MessageHandler(Filters.command, unknown))
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()
