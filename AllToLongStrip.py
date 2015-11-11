__author__ = 'alan.francis'

from PIL import Image
import os
import sys

root_folder = '/Volumes/Personal/Media/Manga/girl_the_wild_s/'
output_folder = 'longstrip'
pathsep = os.path.sep

split = True
extn = '.png'
if len(sys.argv) > 1:
    root_folder = sys.argv[1]
    if len(sys.argv) > 2:
        split = sys.argv[2]

if not root_folder.endswith(pathsep):
    root_folder += pathsep


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
    for each_dir in dirs:
        if output_folder not in each_dir:
            print('Processing', each_dir)
            op_path = root_folder+output_folder+pathsep+each_dir
            if not os.path.exists(op_path):
                os.makedirs(op_path)
            else:
                print(each_dir, ' has already been converted to long strip format, '
                            'to retry delete the folder and try again')
                continue

            for roo, directories, filez in os.walk(os.path.join(root, each_dir)):
                for each_file in filez:
                    if not str(each_file).startswith('.'):
                        append(op_path+pathsep+each_dir+extn, os.path.join(roo, each_file))
