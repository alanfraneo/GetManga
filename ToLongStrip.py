__author__ = 'alan.francis'

from PIL import Image
import os
import sys

root_folder = '/Volumes/Personal/Media/Manga/girl_the_wild_s/Ch 206/'
split = True
extn = '.png'
if len(sys.argv) > 1:
    root_folder = sys.argv[1]
    if len(sys.argv) > 2:
        split = sys.argv[2]

if not root_folder.endswith('/'):
    root_folder += '/'


def append(opfile, ipfile):
    img1 = None
    img1size = [0, 0]
    if os.path.exists(opfile):
        img1 = Image.open(opfile, 'r')
        img1size = img1.size

    img2 = Image.open(ipfile, 'r')
    img2size = img2.size
    img_width = img2size[0]
    if img1size[0] > 0 and img1size[0] > img2size[0]:
        img_width = img1size[0]
    img_height = img1size[1] + img2size[1]

    new_img = Image.new('RGBA', (img_width, img_height))
    if img1 is None:
        new_img.paste(img2, (0, 0))
    else:
        new_img.paste(img1, (0, 0))
        new_img.paste(img2, (0, img1size[1]))
    new_img.save(opfile)


file_list = []
for root, dirs, files in os.walk(root_folder):
    for eachfile in files:
        if not str(eachfile).startswith('.'):
            file_list.append(os.path.join(root, eachfile))

filenamecount = 1
count = 1
for eachfile in file_list:
    if count == 9 and split == True:
        count = 1
        filenamecount += 1
    print('adding', eachfile, '...')
    append(root_folder+str(filenamecount)+extn, eachfile)
    count += 1
