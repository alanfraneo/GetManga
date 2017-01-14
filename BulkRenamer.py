import os


root_folder = '/Volumes/Personal/Media/Manga/'

for manga in os.listdir(root_folder):
    manga_path = os.path.join(root_folder, manga)
    if os.path.isdir(manga_path):
        print(manga_path)
        for chapter in os.listdir(manga_path):
            chapter_path = os.path.join(manga_path, chapter)
            if os.path.isdir(chapter_path):
                print(chapter_path)
                for filename in os.listdir(chapter_path):
                    if '?' in filename:
                        print(filename.split("?")[0])
                        os.rename(os.path.join(chapter_path, filename), os.path.join(chapter_path,filename.split("?")[0]))
