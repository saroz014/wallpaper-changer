import os
import requests
import shutil  # to save image locally
import random
from bs4 import BeautifulSoup


def get_random_page():
    response = requests.get('https://photonepal.travel/most/downloads')
    soup = BeautifulSoup(response.text, features="lxml")
    pagination_tag = soup.find("ul", {"class": "pagination"})
    pages = pagination_tag.find_all('li')
    start = int(pages[1].text)
    end = int(pages[-2].text)
    page = random.randint(start, end)
    return page


def get_random_image():
    page = get_random_page()
    response = requests.get(f'https://photonepal.travel/ajax/downloads?page={page}')
    soup = BeautifulSoup(response.text, features="lxml")
    image_tag = soup.find_all("a", {"class": "item hovercard"}, href=True)
    return random.choice(image_tag)['href']


def save_image():
    image = get_random_image()
    name = image.split('/')[-1]
    response = requests.get(image)
    soup = BeautifulSoup(response.text, features="lxml")
    img = soup.find("img", {"alt": "download_img", "class": "img-responsive img-rounded"})

    # stream = True, to return the stream content.
    image_url = img['src']
    r = requests.get(image_url, stream=True)

    if r.status_code == 200:
        # decode_content = True, to ensure the downloaded image size will not be zero.
        r.raw.decode_content = True

        filename = f"{name}.{image_url.split('.')[-1]}"

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
