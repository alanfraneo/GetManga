__author__ = 'alan.francis'

import requests
from bs4 import BeautifulSoup
import os
import sys

root_url = 'http://tamiltunes.com/ilayaraja-hits-3404-tamil-songs-3.html'
root_folder = 'E:\Music'
folder_name = ''
if len(sys.argv) > 1:
    root_url = sys.argv[1]
    if len(sys.argv) > 2:
        folder_name = sys.argv[2]

page = requests.get(root_url)
if folder_name != '':
    root_folder += os.path.sep + folder_name

# print(page.text)

soup = BeautifulSoup(page.text, 'html.parser')

aList = soup.find_all('a')

# print(aList)

if not os.path.exists(root_folder):
    os.makedirs(root_folder)

for eachA in aList:
    # print(eachA)
    if 'href' in eachA.attrs:
        href = eachA.attrs['href']
        if str(href).endswith('.mp3'):
            filename = root_folder+os.path.sep+eachA.text
            filename = filename.replace(' – TamilWire.com', '')
            filename = filename.replace('\u2013', '-')
            filename = filename.replace('\u2026', '')
            if not os.path.exists(filename):
                print('Downloading', href)
                img = requests.get(href)
                print('saving to', filename)
                f = open(filename, 'wb')
                f.write(img.content)
                f.close()
            else:
                print(filename, 'already downloaded')

print('All mp3 files from', soup.title, 'downloaded successfully')
