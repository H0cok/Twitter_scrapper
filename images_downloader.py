import requests
import os
import json
from constants import *


def download_media(url, directory):
    response = requests.get(url, stream=True)
    if not os.path.exists(IMAGES_DIR_NAME):
        os.makedirs(IMAGES_DIR_NAME)
    with open(directory, 'wb+') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)


def download_img():
    with open(f"output_{ACC_NAME}.json", encoding='utf-8') as file:
        data = json.load(file)
        for key in data.values():
            for idx, video_l in enumerate(key["images"]):
                name = f"{IMAGES_DIR_NAME}/" + key["posted_time"][:10] + " id" + key["tweet_id"] + " #" + str(idx) + ".jpg"
                download_media(video_l, name)


