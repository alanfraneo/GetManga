#  __author__ = "alan.francis"  #

import requests
from bs4 import BeautifulSoup
import os
import sys
from PIL import Image
from multiprocessing import Pool


def is_folder_valid(path_name):
    is_valid = True
    file_list = []
    excluded_extn = ['.txt']
    for root, dirs, files in os.walk(path_name):
        for eachfile in files:
            fname, ext = os.path.splitext(eachfile)
            if not str(eachfile).startswith('.') and ext not in excluded_extn:
                file_list.append(os.path.join(root, eachfile))

    for eachfile in file_list:
        try:
            fimg = Image.open(eachfile, 'r')
            fimg.load()
        except (IOError, OSError) as exc:
            print(eachfile, 'not downloaded properly')
            is_valid = False
        except Exception as e2:
            print(eachfile, 'error')
            is_valid = False
    return is_valid


def download_image_from_page(page):
    pagecontent = requests.get(page)
    pagesoup = BeautifulSoup(pagecontent.text, 'html.parser')
    imagesection = pagesoup.find(id="image")
    img_url = imagesection['src']
    # print(img_url)
    filename = directory + pathsep + 'dummy.png'
    if '?' in img_url:
        filename = directory + pathsep + ((img_url.split('d/'))[1].split('?')[0])
    else:
        filename = directory + pathsep + (img_url.rsplit('/', 1))[1]

    dont_download = False
    if os.path.exists(filename):
        print(filename, 'already downloaded')
        try:
            img = Image.open(filename, 'r')
            img.load()
        except (IOError, OSError) as e:
            print('but file is corrupt')
        else:
            dont_download = True
    if dont_download is False:
        try:
            img = requests.get(img_url)
            print('saving to', filename)
            if os.path.exists(filename):
                os.remove(filename)
            f = open(filename, 'wb')
            f.write(img.content)
            f.close()
        except Exception as ie:
            os.system('say "Manga Download Error"')

# eg root_url: 'http://www.mangahere.co/manga/akame_ga_kiru_zero/c001/'
root_url = 'http://www.mangahere.co/manga/shokugeki_no_soma/c173.1/'
thread_count = 5
if len(sys.argv) > 1:
    root_url = sys.argv[1]
    if len(sys.argv) > 2:
        thread_count = int(sys.argv[2])
# else:
#     print("Incorrect no of parameters passed. format: python3 GetManga.py <chapter_url> <thread_count>")
#     print("e.g.: python3 GetManga.py http://www.mangahere.co/manga/akame_ga_kiru_zero/c001/ 5")
#     exit(0)

manga_name = ((root_url.split('/manga/'))[1].split('/')[0])
print('Manga Name:',manga_name)
firstPage = requests.get(root_url)
manga_num = ((firstPage.text.split('/get_chapters'))[1].split('.js?')[0])
print('Manga #', manga_num)
location = '/Volumes/Personal/Media/Manga/'+manga_name
pathsep = os.path.sep
progressFile = location+pathsep+manga_name+'_progress.txt'
chapters = requests.get('http://www.mangahere.co/get_chapters'+manga_num+'.js')
start = 'var chapter_list = new Array('
end = ');'
chapterListText = ((chapters.text.split(start))[1].split(end)[0])
chapterList = chapterListText.split(sep='\n')
finished_chapters = ['Example Chapter']

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
        name = name.replace('- Fixed', '')
        name = name.replace('&amp;', '&')
        name = name.replace('&#039;', "'")
        directory = location+pathsep+name
        images_valid = False
        already_present = False
        if name in finished_chapters:
            already_present = True
            print('Chapter:', name, 'already downloaded')
            images_valid = is_folder_valid(directory)
            if not images_valid:
                print('but some images are corrupt, downloading again...')

        if not images_valid or not already_present:
            print('Downloading chapter:', name)
            if not os.path.exists(directory):
                os.makedirs(directory)
            url = values[1].replace('"+series_name+"', manga_name)
            url = url.strip()[: -3]
            # print('Name:', name)
            # print('URL:', url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'html.parser')
            select_boxes = soup.find_all('select')
            box = ''
            for select_box in select_boxes:
                if select_box['onchange'] == 'change_page(this)':
                    box = select_box
            pages = []
            for option in box.contents:
                if '\n' != str(option):
                    pages.append(str(option['value']).strip())

            pool = Pool(thread_count)
            pool.map(download_image_from_page, pages)
            pool.terminate()

            finished_chapters.append(name)
            with open(progressFile, mode='a', encoding='UTF-8') as b_file:
                b_file.write(name+'\n')
print(manga_name, 'downloaded successfully')
os.system('say "Manga Download complete"')
