import logging
import os
import youtube_dl
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from settings import TOKEN


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


# Функція, яка викликається при команді /start
def start(update, context):
    """Welcome message handler"""
    welcome_message = "Hello, I'm a YouTube video downloader bot. Please send me the link to the video you want to " \
                      "download."
    update.message.reply_text(welcome_message)


def download_video(update, context):
    # Відправляємо повідомлення про те, що відео завантажується
    message = update.message.text
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            info = ydl.extract_info(message, download=False)
            filename = ydl.prepare_filename(info)
            ydl.download([message])
        update.message.reply_text("Video has been successfully downloaded.")
        send_video(update, context, filename)
        os.remove(filename)
    except:
        update.message.reply_text("This video can not be downloaded.")


def send_video(update, context, filename):
    # Загружаем видео в чат телеграма
    with open(filename, 'rb') as video_file:
        context.bot.send_video(chat_id=update.message.chat_id, video=video_file)


def main():
    # Підключаємося до бота
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, download_video))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
