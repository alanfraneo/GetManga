__author__ = 'alan-1554'

import sys
import os
from PIL import Image
from datetime import datetime

root_folder = '/Volumes/Personal/Media/Manga/girl_the_wild_s/'

if len(sys.argv) > 1:
    root_folder = sys.argv[1]

excluded_extn = ['.txt']

file_list = []

file_check_start_time = datetime.now()
print('Image validation began at', file_check_start_time)


for root, dirs, files in os.walk(root_folder):
    for eachfile in files:
        name, ext = os.path.splitext(eachfile)
        if not str(eachfile).startswith('.') and ext not in excluded_extn:
            file_list.append(os.path.join(root, eachfile))

print('number of files to check:', len(file_list))
errorcount = 0
for eachfile in file_list:
    #if file_list.index(eachfile) != 0 and file_list.index(eachfile) % 100 == 0:
        #print(file_list.index(eachfile), 'files processed')
    img = Image.open(eachfile, 'r')
    try:
        img.load()
    except (IOError, OSError) as e:
        print(eachfile, 'not downloaded properly')
        errorcount += 1
    except Exception as e2:
        print(eachfile, 'error')
        errorcount += 1

file_check_end_time = datetime.now()
print('Image validation ended at', file_check_end_time)
print('Image validation completed in', (file_check_end_time-file_check_start_time))
print('No of files with errors', errorcount)
