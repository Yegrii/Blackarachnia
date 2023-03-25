import os
import logging

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from pytube import YouTube


def download_video(video_link: str) -> str:
    """Downloads the video from YouTube.

    Args:
        video_link: The link to the video.

    Returns:
        The path to the downloaded video.
    """

    # Create a YouTube object with the video link.
    youtube = YouTube(video_link)

    # Get the highest quality stream for the video.
    stream = youtube.streams.get_highest_resolution()

    # Download the video to the current working directory.
    video_path = stream.download()

    return video_path


def start(update: Update, context: CallbackContext) -> None:
    """Handler for the /start command.

    Args:
        update: The Telegram update object.
        context: The Telegram context object.

    Returns:
        None.
    """

    context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! Send me a YouTube link to download a video.")


def download_video_handler(update: Update, context: CallbackContext) -> None:
    """Handler for downloading a video from a YouTube link.

    Args:
        update: The Telegram update object.
        context: The Telegram context object.

    Returns:
        None.
    """

    # Get the video link from the user's message.
    video_link = update.message.text

    # Download the video.
    try:
        video_path = download_video(video_link)
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Video downloaded to {video_path}")
    except Exception as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error downloading video: {e}")


def main() -> None:
    """Initialize the bot.

    Args:
        None.

    Returns:
        None.
    """

    # Get the token from the settings file.
    with open('settings.py', 'r') as f:
        token = f.read().strip().split('=')[1].strip().strip("'")

    # Create the bot.
    bot = Updater(token, use_context=True)

    # Add the start command handler.
    bot.dispatcher.add_handler(CommandHandler('start', start))

    # Add the download video handler.
    bot.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video_handler))

    # Start the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()
