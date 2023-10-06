import json
from twitter_scraper_selenium import scrape_profile
from videos_downloader import download_vid
from images_downloader import download_img
from constants import *

profile = scrape_profile(twitter_username=ACC_NAME, output_format="json", browser="chrome", tweets_count=TWEET_COUNT,
                         headless=HEADLESS)


# Function to convert unicode into correct arabic symbols
def convert_unicode_escapes_to_characters(json_str):
    # Load the JSON string into a Python dictionary
    data = json.loads(json_str)

    # Convert the dictionary back to a JSON string while preserving non-ASCII characters
    unescaped_str = json.dumps(data, ensure_ascii=False)

    return unescaped_str


# Convert Unicode escapes to actual characters and get the string representation of the dictionary
unescaped_str = convert_unicode_escapes_to_characters(profile)

# Saving file
with open(f'output_{ACC_NAME}.json', 'w', encoding='utf-8') as f:
    f.write(unescaped_str)

# Saving all images
download_img()
# Saving all videos
download_vid()



