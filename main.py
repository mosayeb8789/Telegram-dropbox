from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import dropbox
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
DROPBOX_TOKEN = os.getenv("DROPBOX_ACCESS_TOKEN")

def start(update: Update, context: CallbackContext):
    update.message.reply_text("سلام! فایل خود را ارسال کنید.")

def upload_to_dropbox(file_path, file_name):
    dbx = dropbox.Dropbox(DROPBOX_TOKEN)
    with open(file_path, "rb") as f:
        dbx.files_upload(f.read(), f"/{file_name}")
    link = dbx.sharing_create_shared_link_with_settings(f"/{file_name}").url
    return link.replace("?dl=0", "?dl=1")

def handle_file(update: Update, context: CallbackContext):
    file = update.message.document or update.message.photo[-1]
    file_path = file.get_file().download()
    file_name = file.file_name if hasattr(file, 'file_name') else "file.jpg"

    link = upload_to_dropbox(file_path, file_name)
    update.message.reply_text(f"لینک دانلود مستقیم: {link}")

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document | Filters.photo, handle_file))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
