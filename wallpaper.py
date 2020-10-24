import os
import requests
import shutil  # to save image locally
import json
import random


def get_url(page):
    url = f'https://unsplash.com/napi/search/photos?query=nepal&xp=feedback-loop-v2%3Aexperiment&per_page=20&page={page}&orientation=landscape'
    return url


def get_random_page():
    response = requests.get(get_url(1))
    response_json = json.loads(response.text)
    total_pages = response_json['total_pages']
    page = random.randint(1, total_pages)
    return page


def get_random_image():
    page = get_random_page()
    response = requests.get(get_url(page))
    response_json = json.loads(response.text)
    image = random.choice(response_json['results'])['urls']['raw']
    return image


def save_image():
    image = get_random_image()
    # stream = True, to return the stream content.
    r = requests.get(image, stream=True)

    if r.status_code == 200:
        # decode_content = True, to ensure the downloaded image size will not be zero.
        r.raw.decode_content = True
        filename = "wallpaper.jpg"

        with open(filename, 'wb') as f:
            shutil.copyfileobj(r.raw, f)

        return filename
    else:
        print('Unable to download image')


def set_wallpaper():
    filename = save_image()
    cmd = f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri 'file://{os.getcwd()}/{filename}'"
    os.system(cmd)


if __name__ == '__main__':
    set_wallpaper()
