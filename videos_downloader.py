import requests
import json
import os
from constants import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from twitter_scraper_selenium import driver_initialization


def get_video_link(driver, url_to_fetch):
    # Navigate to the website
    driver.get('https://ru.savefrom.net/240/')

    # Find the input element and input the URL
    input_element = driver.find_element(By.XPATH, '//*[@id="sf_url"]')
    input_element.send_keys(url_to_fetch)
    input_element.send_keys(Keys.RETURN)  # Hit Enter after entering the URL

    # Wait for 1.5 seconds
    try:
        element_present = EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '.mp4')]"))
        WebDriverWait(driver, 3.5).until(element_present)

        video_link_element = driver.find_element(By.XPATH, "//a[contains(@href, '.mp4')]")
        video_link = video_link_element.get_attribute('href')
    except TimeoutException:
        video_link = None

    # Return the first link (or None if no link is found)
    return video_link


def download_video_from_url(url, output_filename):
    if not os.path.exists(VIDEOS_DIR_NAME):
        os.makedirs(VIDEOS_DIR_NAME)
    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)


# Main function to download videos from existing json file
def download_vid():
    driver = driver_initialization.Initializer("chrome", HEADLESS)  # Use "firefox" if you're using Firefox
    driver = driver.init()
    with open(f"output_{ACC_NAME}.json", encoding='utf-8') as file:
        data = json.load(file)
        for key in data.values():
            if key["videos"]:
                name = f"{VIDEOS_DIR_NAME}/" + key["posted_time"][:10] + " id" + key["tweet_id"] + ".mp4"
                video_link = get_video_link(driver, key["tweet_url"])
                if video_link:
                    download_video_from_url(video_link, name)
    driver.close()
