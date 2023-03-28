import os
import logging
import re
import requests
import telegram
from pytube import YouTube
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from settings import TOKEN


# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Google Drive credentials
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Video download directory
DOWNLOAD_DIR = 'downloads'


def start(update, context):
    """Welcome message handler"""
    welcome_message = "Hello, I'm a video downloader bot. Please send me the link to the video you want to download."
    update.message.reply_text(welcome_message)


def download_youtube_video(update, context):
    """Downloads video from YouTube"""
    message = update.message.text
    try:
        # Validate YouTube video URL
        youtube_regex = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"
        match = re.match(youtube_regex, message)
        if not match:
            update.message.reply_text("Invalid YouTube video URL.")
            return

        # Download video from YouTube
        update.message.reply_text("Downloading YouTube video...")
        yt = YouTube(message, on_progress_callback=progress_callback)
        video_title = yt.title
        video_stream = yt.streams.get_highest_resolution()
        video_file = video_stream.download(DOWNLOAD_DIR, filename=f"{video_title}.mp4")
        update.message.reply_text("Video downloaded from YouTube.")

        # Upload video to Telegram and delete from disk
        upload_video(update, context, video_file)

    except Exception as e:
        update.message.reply_text(f"Error: {e}")


def download_google_drive_video(update, context):
    """Downloads video from Google Drive"""
    message = update.message.text
    try:
        # Validate Google Drive video URL
        drive_regex = r"^(https?\:\/\/)?drive\.google\.com\/file\/d\/.+"
        match = re.match(drive_regex, message)
        if not match:
            update.message.reply_text("Invalid Google Drive video URL.")
            return

        # Download video from Google Drive
        update.message.reply_text("Downloading Google Drive video...")
        file_id = message.split("/")[5]
        file = drive.CreateFile({'id': file_id})
        video_title = file['title']
        video_file = os.path.join(DOWNLOAD_DIR, f"{video_title}.mp4")
        file.GetContentFile(video_file)
        update.message.reply_text("Video downloaded from Google Drive.")

        # Upload video to Telegram and delete from disk
        upload_video(update, context, video_file)

    except Exception as e:
        update.message.reply_text(f"Error: {e}")


def upload_video(update, context, video_file):
    """Uploads video to Telegram and deletes from disk"""
    update.message.reply_text("Uploading video to Telegram...")
    bot = telegram.Bot(token=TOKEN)
    bot.send_video(chat_id=update.message.chat_id, video=open(video_file, 'rb'), timeout=120)
    os.remove(video_file)
    update.message.reply_text("Video has been uploaded to Telegram.")


def progress_callback(stream, chunk, bytes_remaining):
    """Progress callback function for PyTube"""
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = round((bytes_downloaded / total_size) * 100, 2)
    print(f"{percentage}% downloaded")


def main():
    """Main function"""
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler('start', start))
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, download_youtube_video))
    dispatcher.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, download_google_drive_video))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
