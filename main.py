from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram.ext.filters import Filters

def start(update, context):
    update.message.reply_text('Hello!')

def echo(update, context):
    update.message.reply_text(update.message.text)

def main():
    # جایگزینی توکن خود را با ربات تلگرام
    updater = Updater("YOUR_BOT_TOKEN", use_context=True)
    
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))  # استفاده از فیلتر
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
