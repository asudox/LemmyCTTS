from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as fx_options
from selenium.webdriver.chrome.options import Options as ch_options
from selenium.webdriver.edge.options import Options as eg_options
from selenium.webdriver.safari.options import Options as sf_options
from typing import List
from time import sleep as tsleep
from loguru import logger

def screenshotLemmy(instance_url: str, post_id: str, comment_ids: List[str], jwt: str, browser: str) -> None:
    match browser.upper():
        case "FIREFOX":
            browser_options = fx_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument("--no-extensions")
            driver = webdriver.Firefox(options=browser_options)
        case "CHROME":
            browser_options = ch_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument("--no-extensions")
            driver = webdriver.Chrome(options=browser_options)
        case "EDGE":
            browser_options = eg_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument("--no-extensions")
            driver = webdriver.Edge(options=browser_options)
        case "SAFARI":
            browser_options = sf_options()
            browser_options.add_argument("--headless")
            browser_options.add_argument("--no-extensions")
            driver = webdriver.Safari(options=browser_options)
        case _:
            logger.error("Browser of choice not valid. Please set one of the followings: firefox, edge, chrome, safari")
            exit()

    driver.get(url=instance_url)
    try:
        driver.add_cookie({"name": "jwt", "domain": instance_url.split("://")[1], "value": jwt})
    except Exception as e:
        logger.warning(f"Could not add jwt cookie to the session, continuing without logging into the bot\n{e.__class__.__name__}: {e}")
    progress = 0
    driver.get(url=instance_url + f"/post/{post_id}")
    try:
        post_body = driver.find_element(by=By.XPATH, value="/html/body/div/div/div[2]/div/div/div/main/div[1]/div[2]")
        post_body.screenshot(f"screenshots/post.png")
        logger.success("Successfully took a screenshot of the post")
    except Exception as e:
        logger.error(f"An error occurred while taking a screenshot of the post\n{e.__class__.__name__}: {e}")
        exit()
    logger.info("Taking screenshots of comments")
    for comment_id in comment_ids:
        progress += 1
        try:
            tsleep(0.5)
            driver.get(url=instance_url + f"/comment/{comment_id}")
            body = driver.find_element(by=By.ID, value=f"comment-{comment_id}")
            body.screenshot(f"screenshots/comment_{comment_id}.png")
            logger.success(f"Successfully took a screenshot of the comment ({progress}/{len(comment_ids)}): {comment_id}")
        except Exception as e:
            logger.error(f"An error occurred while taking screenshots of comments\n{e.__class__.__name__}: {e}")
            exit()
    driver.close()
    logger.success("Successfully took screenshots of all the comments")
