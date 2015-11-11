__author__ = 'alan_francis'

import requests
from bs4 import BeautifulSoup
import os
import sys
import json
import urllib.parse


def zerofill(number):
    if len(number) == 1:
        return '00'+str(number)
    elif len(number) == 2:
        return '0'+str(number)
    else:
        return str(number)


root_url = 'http://www.mangareader.net/naruto/1'  # Sample url: 'http://www.mangahere.co/manga/akame_ga_kiru_zero/c001/'
root_location = '/Volumes/Personal/Media/Manga/'
pathsep = os.path.sep

if len(sys.argv) > 1:
    root_url = sys.argv[1]

manga_name = ((root_url.split('mangareader.net/'))[1].split('/')[0])
print('Manga Name:', manga_name)
location = root_location+pathsep+manga_name
progressFile = location+pathsep+manga_name+'_progress.txt'

firstPage = requests.get(root_url)
# print(firstPage.text)
manga_id = ((firstPage.text.split("['mangaid'] ="))[1].split(';')[0]).strip()
print('Manga Id: #'+manga_id)

# http://www.mangareader.net/actions/selector/?id=93&which=182259
chaptersJson = json.loads(requests.get('http://www.mangareader.net/actions/selector/?id='+manga_id+'&which=0').text)
# print(chaptersJson)

finished_chapters = ['Example Chapter']

if not os.path.exists(location):
    os.makedirs(location)

if not os.path.exists(progressFile):
    print('Fresh start')
else:
    with open(progressFile, encoding='UTF-8') as a_file:
        for line in a_file:
            finished_chapters.append(line.strip())

for chapter in chaptersJson:
    name = 'Ch '+zerofill(chapter['chapter'])+' - ' + chapter['chapter_name']
    name = name.replace('&#039;', '\'')
    name = name.replace('&amp;', '&')
    url = 'http://www.mangareader.net'+chapter['chapterlink']
    if name in finished_chapters:
        print('Chapter:', name, 'already downloaded')
    else:
        print('Downloading chapter:', name)
        directory = location+pathsep+name
        if not os.path.exists(directory):
            os.makedirs(directory)
        # print('chapter:', chapter)
        print('Name:', name)
        print('URL:', url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        box = soup.find(id='pageMenu')
        # print(box.contents)
        pages = []
        for option in box.contents:
            if '\n' != str(option):
                # print('page url:', option['value'])
                pages.append(str(option['value']).strip())
        # print(pages)

        for eachPage in pages:
            pageContent = requests.get('http://www.mangareader.net'+eachPage)
            # print(pageContent.text);
            pageSoup = BeautifulSoup(pageContent.text, 'html.parser')
            imageSection = pageSoup.find(id="img")
            # imgTag = imageSection.img[1]
            img_url = imageSection['src']
            print(img_url)
            filename = directory + pathsep + 'dummy.png'
            if '?v' in img_url:
                filename = directory+pathsep + ((img_url.split('d/'))[1].split('?v')[0])
            else:
                lists = img_url.rsplit('/', 1)
                filename = directory+pathsep + lists[1]

            if os.path.exists(filename):
                print(filename, 'already downloaded')
            else:
                img = requests.get(img_url)
                print('saving to', filename)
                f = open(filename, 'wb')
                f.write(img.content)
                f.close()

        finished_chapters.append(name)
        with open(progressFile, mode='a', encoding='UTF-8') as b_file:
            b_file.write(name+'\n')
print(manga_name, 'downloaded successfully')


