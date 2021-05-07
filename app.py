import os
import requests
import tweepy

from bs4 import BeautifulSoup
from flask import Flask
from os import remove
from os.path import isfile
from requests import get
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env


app = Flask(__name__)


def get_images() -> list:
    headers = {"User-Agent": os.environ['USER_AGENT']}

    try:
        res = get(os.environ['URL'], headers=headers)

        soup = BeautifulSoup(res.text, 'html.parser')
        img_tags = soup.find_all('img')

        urls = [img['src'] for img in img_tags]
        url_images = []

        for url in urls:
            if 'rcg-cdn.explosm.net' in url:
                url_images.append(url)

        for idx in range(len(url_images)):
            res = get(url_images[idx])
            file = open(f'/tmp/{url_images[idx][-16:]}', "wb")
            file.write(res.content)
            file.close()
        res.raise_for_status()

    except requests.exceptions.HTTPError as error:
        raise error

    return [name_images[-16:] for name_images in url_images]


def validate_images(list_images: list) -> bool:
    for img in list_images:
        if isfile(f'/tmp/{img}') is False:
            return False

    return True


def delete_images(list_images: list) -> None:
    for img in list_images:
        remove(f'/tmp/{img}')


def post_tweet(images: list) -> bool:
    # Authenticate to Twitter
    consumer_key = os.environ['CONSUMER_KEY']
    consumer_secret = os.environ['CONSUMER_SECRET']
    access_token = os.environ['ACCESS_TOKEN']
    access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    msg = os.environ['MESSAGE']

    try:
        path_images = []
        media_ids = []

        if validate_images(images):
            for img in images:
                path_images.append(f'/tmp/{img}')

        # Upload images and get media_ids
        for filename in path_images:
            res = api.media_upload(filename)
            media_ids.append(res.media_id)

        # Tweet with multiple images
        api.update_status(status=f'{msg}✨', media_ids=media_ids)

        delete_images(images)

    except tweepy.error.TweepError as Err:
        delete_images(images)
        print(Err)

        return False

    return True


@app.route('/')
def hello_world():
    list_images = get_images()
    post_tweet(list_images)

    return 'The meme has been published'


if __name__ == '__main__':
    app.run()
