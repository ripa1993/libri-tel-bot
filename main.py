import logging
import os
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext

import libritel as lt

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

allowed_ids = [-278919632, 110247988]


def allowed_chat(update: Update) -> bool:
    print("Chat id: " + str(update.effective_chat.id))
    return update.effective_chat.id in allowed_ids


def search_cmd(update: Update, context: CallbackContext) -> None:
    """Search libri.tel for books"""
    if not allowed_chat(update):
        return None

    search_query = str.join(" ", context.args[0:])
    results = lt.search(search_query)

    keyboard = [[KeyboardButton("/get " + r.url)] for r in results]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    update.message.reply_text('Scegli ⤵️', reply_markup=reply_markup)


def get_cmd(update: Update, context: CallbackContext) -> None:
    """Get download link from libri.tel"""
    if not allowed_chat(update):
        return None

    libri_tel_url = context.args[0]
    download_link = lt.get_download_link(lt.SearchResult(name="", url=libri_tel_url))
    update.message.reply_text(download_link)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    port = int(os.environ["PORT"])
    token = os.environ["TELEGRAM_TOKEN"]

    updater = Updater(token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("search", search_cmd))
    dispatcher.add_handler(CommandHandler("get", get_cmd))

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0", port=port, url_path=token)
    updater.bot.set_webhook("https://libritelbot.herokuapp.com/" + token)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
