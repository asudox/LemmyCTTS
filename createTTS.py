import re
import tldextract
from gtts import gTTS
from loguru import logger
from validators import url as isURL
from time import sleep as tsleep

urlextractor = tldextract.TLDExtract()

def cleanText(text: str) -> str: #  todo
    found_urls = [word for word in text.split() if isURL(word)]
    if found_urls:
        shortened_urls = [f"{urlextractor(url).domain}.{urlextractor(url).suffix}" for url in found_urls]
        modified_urls = list(map(lambda x: (x, f"{x[:20]}...{x.split('.')[1]}") if len(x) > 20 else (x,x), shortened_urls))
        cleaned_text = None
        for old_url, modified_url in modified_urls:
            cleaned_text = text.replace(old_url, modified_url) # todo: get rid of http or https
        return cleaned_text
    else:
        return text


def createTTS(comment_datas: dict, post_name: str) -> None:
    progress = 0
    try:
        gTTS(post_name).save(f"tts/post_tts.mp3")
        logger.success(f"Successfully generated the post TTS file")
    except Exception as e:
        logger.error(f"An error occurred while converting text-to-speech\n{e.__class__.__name__}: {e}")
        exit()
    for comment_id, comment_content in comment_datas.items():
        tsleep(0.5)
        comment_content = cleanText(comment_content)
        progress += 1
        try:
            gTTS(comment_content).save(f"tts/comment_tts_{comment_id}.mp3")
            logger.success(f"Successfully generated a TTS file ({progress}/{len(comment_datas)}): {comment_id}")
        except Exception as e:
            logger.error(f"An error occurred while converting text-to-speech\n{e.__class__.__name__}: {e}")
            exit()
    logger.success("Successfully generated all TTS files")
