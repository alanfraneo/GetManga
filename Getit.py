__author__ = 'alan-1554'

import requests
from bs4 import BeautifulSoup
import os

manga_name = 'shokugeki_no_soma'  # 'fairy_tail';
manga_num = '12114'  # 246
location = '/Volumes/Personal/Media/Manga/'+manga_name
pathsep = '/'
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
        values = chapter.split(',')
        name = values[0].strip()[2:-1]
        name = name.replace(':', '-')
        name = name.replace('&quot;', '')
        if name in finished_chapters:
            print('Chapter:',name, 'already downloaded');
        else:
            print('Downloading chapter:', name)
            directory = location+pathsep+name
            if not os.path.exists(directory):
                os.makedirs(directory)

            url = values[1].replace('"+series_name+"',manga_name)
            url = url.strip()[1: -2]
            # print('Name:', name)
            # print('URL:', url)
            print(url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            select_boxes = soup.find_all('select')
            box = ''
            for select_box in select_boxes:
                if select_box['onchange'] == 'change_page(this)':
                    box = select_box;
            # print(box.contents)
            pages = []
            for option in box.contents:
                if '\n' != str(option):
                    # print('page url:', option['value'])
                    pages.append(str(option['value']).strip())
            # print(pages)

            for eachPage in pages:
                pageContent = requests.get(eachPage)
                pageSoup = BeautifulSoup(pageContent.text, 'html.parser')
                imageSection = pageSoup.find(id="viewer")
                imgTag = imageSection.img
                img_url = imgTag['src'];
                print(img_url)
                filename = directory+pathsep+ ((img_url.split('d/'))[1].split('?v')[0])
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