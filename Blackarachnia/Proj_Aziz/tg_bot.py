import os
from telegram.ext import Updater, CommandHandler
import youtube_dl
from config import token

# Создайте функцию для скачивания видео с YouTube:
def download_video(link):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])


# Создайте функцию для обработки команды /download в Telegram:

def download(update, context):
    link = update.message.text.split(" ")[1]
    download_video(link)
    update.message.reply_text("Видео успешно скачано!")

# Инициализируйте Updater и добавьте обработчик команды /download:

updater = Updater(token, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("download", download))

# Запустите бота:

updater.start_polling()
updater.idle()