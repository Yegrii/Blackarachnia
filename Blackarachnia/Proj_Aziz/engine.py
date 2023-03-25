import logging

import youtube_dl


def download_video(video_link):
    """Downloads the video from YouTube.

    Args:
        video_link: The link to the video.

    Returns:
        The path to the downloaded video.
    """

    # Get the video ID.
    video_id = youtube_dl.YoutubeDL({}).extract_video_id(video_link)

    # Try to download the video.
    try:
        with youtube_dl.YoutubeDL({}) as ydl:
            ydl.download([video_id])
            return ydl.download_dir()
    except:
        return None


def main():
    """Initialize the bot.

    Args:
        None

    Returns:
        None
    """

    # Get the token from the settings file.
    token = '1111111111111111111'

    # Create the bot.
    bot = Updater(token, use_context=True)

    # Add the start command handler.
    bot.dispatcher.add_handler(CommandHandler('start', start))

    # Add the download video handler.
    bot.dispatcher.add_handler(MessageHandler(Filters.text, download_video))

    # Start the bot.
    bot.start_polling()
    bot.idle()


if __name__ == '__main__':
    main()