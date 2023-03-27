import os
import logging
import shutil
import pytube
import telegram
from settings import TOKEN

from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# встновлюємо логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


# функція, яка буде викликатися при команді /start
def start(update: Update, context: CallbackContext) -> None:
    # створюємо клавіатуру з однією кнопкою
    button = [['Будь ласка, надішліть посилання на відео']]
    reply_markup = telegram.ReplyKeyboardMarkup(button, resize_keyboard=True)

    # відправляємо користувачу повідомлення та показуємо клавіатуру з кнопкою
    update.message.reply_text('Привіт! Я бот, який допоможе тобі завантажити відео з YouTube =)',
                              reply_markup=reply_markup)


# функція, яка буде викликатися при отриманні посилання на відео
def download_video(update: Update, context: CallbackContext) -> None:
    # відправляємо користувачу повідомлення про те, що починаємо завантажувати відео
    update.message.reply_text('Залишилось трохи почекати...')

    # отримуємо посилання на відео
    video_url = update.message.text.strip()

    try:
        # створюємо екземпляр YouTube
        youtube = pytube.YouTube(video_url)

        # отримуємо потік з найвищим розширенням
        stream = youtube.streams.get_highest_resolution()

        # завантажуємо відео
        stream.download()

        # переміщуємо відео в папку 'video'
        video_filename = stream.default_filename
        video_path = os.path.join(os.getcwd(), video_filename)
        new_video_path = os.path.join(os.getcwd(), 'video', video_filename)
        shutil.move(video_path, new_video_path)

        # відправляємо користувачу повідомлення про те, що відео успішно завантажено
        update.message.reply_text("Вітаю! Відео успішно завантажено!")

    except pytube.exceptions.PytubeError as e:
        # відправляємо користувачу повідомлення про те, що виникла помилка при завантаженні відео
        update.message.reply_text(f'Виникла помилка при завантаженні відео: {e}')


# функція, яка буде викликатися при отриманні будь-якого повідомлення
def echo(update: Update, context: CallbackContext) -> None:
    # створюємо клавіатуру з однією кнопкою
    button = [['Будь ласка, надішліть посилання на відео']]
    reply_markup = telegram.ReplyKeyboardMarkup(button, resize_keyboard=True)

    # відправляємо користувачу повідомлення та показуємо клавіатуру з кнопкою
    update.message.reply_text('Вибач, але я не знаю що тобі на це відповісти =(', reply_markup=reply_markup)


def main() -> None:
    # створюємо екземпляр Updater
    updater = Updater(TOKEN)

    # отримуємо диспетчер бота
    dispatcher = updater.dispatcher

    # регіструємо обробник команди /start
    dispatcher.add_handler(CommandHandler('start', start))

    # регіструємо обробник посилання на відео
    dispatcher.add_handler(MessageHandler(Filters.regex(r'^https://www.youtube.com/watch\?v='), download_video))

    # регіструємо обробник будь-якого повідомлення
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    # запускаємо бота
    updater.start_polling()

    # зупиняємо бота, коли натиснуто Ctrl + C
    updater.idle()


if __name__ == '__main__':
    main()