import os
from loguru import logger
from random import choice as rchoice
from moviepy.editor import VideoFileClip, ImageClip, AudioFileClip, CompositeVideoClip, CompositeAudioClip, concatenate_videoclips, concatenate_audioclips
from moviepy.video.fx.resize import resize as vresize
from moviepy.audio.fx.volumex import volumex as avolumex

def createLemmyVideo(post_id: str) -> str:
    logger.info("Creating Lemmy video")
    comment_screenshots = os.listdir("screenshots")
    comment_screenshots.remove("post.png") # remove post screenshot from comments
    comment_screenshots_len = len(comment_screenshots)
    video_parts_folder = "video/parts/"
    progress = 0

    background_music: AudioFileClip  = avolumex(AudioFileClip(f"background/music/{rchoice(os.listdir('background/music'))}"), 0.2) # random background music
    transition_effect: VideoFileClip = VideoFileClip("background/transition.mp4")
    background_image: ImageClip = ImageClip("background/background.png")

    def makeVideoPart(tts_file: AudioFileClip, comment_screenshot: ImageClip, no_transition: bool = False) -> CompositeVideoClip:
        duration = tts_file.duration

        # configure comment screenshot
        comment_screenshot = comment_screenshot.set_position("center")
        comment_screenshot = comment_screenshot.set_duration(duration)
        comment_screenshot = vresize(comment_screenshot, width=1800)

        to_concatenate_audios = [tts_file]
        to_concatenate_videos = [background_image.set_duration(duration)]
        if not no_transition:
            to_concatenate_audios.append(transition_effect.audio.set_start(duration))
            to_concatenate_videos.append(transition_effect.set_start(duration))

        video_part_audio = concatenate_audioclips(to_concatenate_audios)
        video_part = concatenate_videoclips(to_concatenate_videos)
        video_part = video_part.set_audio(video_part_audio)
        video_part = CompositeVideoClip([video_part, comment_screenshot])
        return video_part

    def makeFinalVideo() -> None:
        logger.info("Adding together video parts to make the final video")
        video_parts = list(map(lambda x: VideoFileClip(f"video/parts/{x}"), os.listdir("video/parts/")))
        video_parts.reverse() # reverse to get the post video part on the first place
        final_video = concatenate_videoclips(video_parts)
        duration = final_video.duration
        final_video_audio = CompositeAudioClip([background_music.set_duration(duration), final_video.audio])
        final_video = final_video.set_audio(final_video_audio)
        final_video.write_videofile(f"video/final_video_{post_id}.mp4", audio=True, fps=10, logger=None)
        final_video.close()
        logger.success("Successfully created the final video. Final video can be found in the video folder")

    # make and write post video part
    try:
        post_video_part = makeVideoPart(AudioFileClip("tts/post_tts.mp3"), ImageClip("screenshots/post.png"), no_transition=True)
    except Exception as e:
        logger.error(f"An error occurred while trying to make the post video part\n{e.__class__.__name__}: {e}")
        exit()
    try:
        post_video_part.write_videofile(f"{video_parts_folder}post_video_part.mp4", audio=True, fps=10, logger=None)
        post_video_part.close()
        logger.success("Successfully created the post video part")
    except Exception as e:
        logger.error(f"An error occurred while trying to save the post video part\n{e.__class__.__name__}: {e}")
        exit()



    # make and write video_part for each comment
    for comment_screenshot in comment_screenshots:
        progress += 1
        comment_id = comment_screenshot.split('_')[1].split('.')[0]
        try:
            comment_video_part = makeVideoPart(AudioFileClip(f"tts/comment_tts_{comment_id}.mp3"), ImageClip(f"screenshots/{comment_screenshot}"), no_transition=False if comment_screenshots_len > 1 else True)
        except Exception as e:
            logger.error(f"An error occurred while trying to make video part\n{e.__class__.__name__}: {e}")
            exit()
        try:
            comment_video_part.write_videofile(f"{video_parts_folder}comment_video_part_{comment_id}.mp4", audio=True, fps=10, logger=None)
            comment_video_part.close()
            comment_screenshots.remove(comment_screenshot)
            logger.success(f"Successfully created a video part ({progress}/{comment_screenshots_len}): {comment_id}")
        except Exception as e:
            logger.error(f"An error occurred while saving a video part\n{e.__class__.__name__}: {e}")
            exit()
    try:
        makeFinalVideo()
    except Exception as e:
        logger.error(f"An error occurred while trying to make the final video\n{e.__class__.__name__}: {e}")
        exit()
