__author__ = 'alan-1554'

'''
todo: build a html web server, which will display images in a folder,
including sub folders as displayed in a continuous fashion with navigation


Approx steps:
1. read all the folder and file names
2. Make chapters or albums of folders and each file arranged using name or date modified
3. put them in a html framework somehow and show them
4. make them avialable in a web server so that we can use it in other devices. i.e my ipad

'''

import os


root_folder = '/Volumes/Personal/Media/Manga/girl_the_wild_s'
pathsep = '/'
server_folder = root_folder+pathsep+'httpserver'
html_file = server_folder+pathsep+'htmlfile.html'

if os.path.exists(server_folder):
    os.removedirs(server_folder)

os.mkdir(server_folder)

file_list = []

for root, dirs, files in os.walk(root_folder, topdown=True):
    for ffile in files:
        file_list.append(os.path.join(root, ffile))

with open(html_file, mode='a', encoding='UTF-8') as htmlfile:
    htmlfile.write("<html><body>")
    for each_file in file_list:
        htmlfile.write("<a href='"+file_list)



