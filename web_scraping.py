import os
import random
import requests
from bs4 import BeautifulSoup

def download_images(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    entry_contents = soup.find_all('div', class_='entry-content')
    figures = entry_contents[0].find_all('figure')

    for figure in figures:
        link = figure.find('img')
        if link and 'src' in link.attrs:
            img_url = link['src']
            img_filename = os.path.join('dataset', img_url.split('/')[-1])

            if os.path.exists(img_filename):
                base, ext = os.path.splitext(img_filename)
                img_filename = f"{base}_{random.randint(100, 999)}{ext}"

            try:
                img_response = requests.get(img_url)
                with open(img_filename, 'wb') as img_file:
                    img_file.write(img_response.content)
                print(f"İndirildi: {img_filename}")
            except Exception as e:
                print(f"Hata: {img_url} indirilemedi - {e}")

import logging
import os
import random

import requests
from bs4 import BeautifulSoup


def download_images(url):
    if not os.path.exists('dataset'):
        os.makedirs('dataset')
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    column_blocks = soup.find_all('div', class_='wp-block-columns')
    image_count = 0
    for block in column_blocks:
        columns = block.find_all('div', class_='wp-block-column')
        for column in columns:
            figures = column.find_all('figure', class_='wp-block-image')
            for figure in figures:
                link = figure.find('a')
                if link and 'href' in link.attrs:
                    image_url = link['href']
                    link_strings = image_url.split('/')
                    filename = os.path.join('dataset', link_strings[-1])
                    if os.path.exists(filename):
                        base, ext = os.path.splitext(filename)
                        filename = f"{base}_{random.randint(100, 999)}{ext}"
                    try:
                        img_response = requests.get(image_url)
                        with open(filename, 'wb') as f:
                            f.write(img_response.content)
                        print(f"İndirildi: {filename}")
                        image_count += 1
                    except Exception as e:
                        print(f"Hata: {image_url} indirilemedi - {e}")
                link = figure.find('img')
                if link and 'src' in link.attrs:
                    img_url = link['src']
                    img_filename = os.path.join('dataset', img_url.split('/')[-1])
                    if os.path.exists(img_filename):
                        base, ext = os.path.splitext(img_filename)
                        img_filename = f"{base}_{random.randint(100, 999)}{ext}"
                    try:
                        img_response = requests.get(img_url)
                        with open(img_filename, 'wb') as img_file:
                            img_file.write(img_response.content)
                        print(f"İndirildi: {img_filename}")
                        image_count += 1
                    except Exception as e:
                        print(f"Hata: {img_url} indirilemedi - {e}")

    print(f"Toplam {image_count} resim indirildi.")
