import os
from loguru import logger

background_video_path = "background/random_background.mp4"
screenshots_path = "screenshots/"
tts_path = "tts/"
video_parts_path = "video/parts/"

def cleanup() -> None:
    # remove background video
    logger.info("Cleaning up")

    # for later use
    # try:
    #     os.remove(background_video_path)
    # except Exception as e:
    #     logger.error(f"An error occurred while removing the background video. Please remove manually!\n{e.__class__.__name__}: {e}")

    # remove screenshots
    try:
        for file in os.listdir(screenshots_path):
            os.remove(screenshots_path + file)
    except Exception as e:
        logger.error(f"An error occurred while cleaning up the screenshots folder. Please cleanup manually!\n{e.__class__.__name__}: {e}")

    # remove video parts
    try:
        for file in os.listdir(video_parts_path):
            os.remove(video_parts_path + file)
    except Exception as e:
        logger.error(f"An error occurred while cleaning up the video parts folder. Please cleanup manually!\n{e.__class__.__name__}: {e}")

    # remove tts files
    try:
        for file in os.listdir(tts_path):
            os.remove(tts_path + file)
    except Exception as e:
        logger.error(f"An error occurred while cleaning up the TTS folder. Please cleanup manually!\n{e.__class__.__name__}: {e}")
    logger.success("Cleanup done")
