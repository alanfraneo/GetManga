#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3.4
__author__ = 'alan-1554'

import requests
from bs4 import BeautifulSoup
import os
import sys
from PIL import Image

root_url = ''  # Sample url: 'http://www.mangahere.co/manga/akame_ga_kiru_zero/c001/'
if len(sys.argv[1]) != 0:
    root_url = sys.argv[1]

manga_name = ((root_url.split('/manga/'))[1].split('/')[0])
print('Manga Name:',manga_name)
firstPage = requests.get(root_url);
manga_num = ((firstPage.text.split('/get_chapters'))[1].split('.js?')[0])
print('Manga #', manga_num)
location = '/Volumes/Personal/Media/Manga/'+manga_name
pathsep = os.path.sep
progressFile = location+pathsep+manga_name+'_progress.txt';
chapters = requests.get('http://www.mangahere.co/get_chapters'+manga_num+'.js')
start = 'var chapter_list = new Array(';
end = ');'
chapterListText = ((chapters.text.split(start))[1].split(end)[0])
# print(chapterListText)
chapterList = chapterListText.split(sep='\n')
# print(chapterList)
finished_chapters = ['Example Chapter'];

if not os.path.exists(location):
    os.makedirs(location)

if not os.path.exists(progressFile):
    print('Fresh start')
else:
    with open(progressFile, encoding='UTF-8') as a_file:
        for line in a_file:
            finished_chapters.append(line.strip())

for chapter in chapterList:
    if len(chapter) > 0 and ',' in chapter:
        values = chapter.split('","')
        name = values[0].strip()[2:]
        name = name.replace(':', '-')
        name = name.replace('&quot;', '')
        if name in finished_chapters:
            print('Chapter:', name, 'already downloaded')
        else:
            print('Downloading chapter:', name)
            directory = location+pathsep+name
            if not os.path.exists(directory):
                os.makedirs(directory)
            # print('chapter:', chapter)
            url = values[1].replace('"+series_name+"',manga_name)
            url = url.strip()[: -3]
            # print('Name:', name)
            # print('URL:', url)
            print("url:", url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            select_boxes = soup.find_all('select')
            box = ''
            for select_box in select_boxes:
                if select_box['onchange'] == 'change_page(this)':
                    box = select_box
            # print(box.contents)
            pages = []
            for option in box.contents:
                if '\n' != str(option):
                    # print('page url:', option['value'])
                    pages.append(str(option['value']).strip())
            # print(pages)

            for eachPage in pages:
                pageContent = requests.get(eachPage)
                # print(pageContent.text);
                pageSoup = BeautifulSoup(pageContent.text, 'html.parser')
                imageSection = pageSoup.find(id="image")
                # imgTag = imageSection.img[1]
                img_url = imageSection['src']
                print(img_url)
                filename = directory + pathsep + 'dummy.png'
                if '?v' in img_url:
                    filename = directory+pathsep + ((img_url.split('d/'))[1].split('?v')[0])
                else:
                    lists = img_url.rsplit('/', 1)
                    filename = directory+pathsep + lists[1]

                dont_download = False
                if os.path.exists(filename):
                    print(filename, 'already downloaded')
                    img = Image.open(filename, 'r')
                    try:
                        img.load()
                    except (IOError, OSError) as e:
                        print('but file is corrupt')
                    else:
                        dont_download = True
                if dont_download is False:
                    img = requests.get(img_url)
                    print('saving to', filename)
                    f = open(filename, 'wb')
                    f.write(img.content)
                    f.close()
            finished_chapters.append(name)
            with open(progressFile, mode='a', encoding='UTF-8') as b_file:
                b_file.write(name+'\n')
print(manga_name, 'downloaded successfully')