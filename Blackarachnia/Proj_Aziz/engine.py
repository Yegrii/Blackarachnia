import logging
# import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import youtube_dl
from settings import TOKEN
# import ssl

# ssl._create_default_https_context = ssl._create_unverified_context
# os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Functions
def start(update, context):
    """Welcome message handler"""
    welcome_message = "Hello, I'm a YouTube video downloader bot. Please send me the link to the video you want to download."
    update.message.reply_text(welcome_message)

def download_video(update, context):
    """Downloads video from YouTube"""
    message = update.message.text
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            ydl.download([message])
        update.message.reply_text("Video has been successfully downloaded.")
    except:
        update.message.reply_text("This video can not be downloaded.")

def main():
    """Initialize bot"""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, download_video))
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
    main()
