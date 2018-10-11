# -*- coding: utf-8 -*-
from os import listdir, walk, system, chdir
from os.path import isfile, join

# -c:v hevc
# -ss
template_command = 'ffmpeg -i "concat:{}" -c:v libx264 -r 25 -crf 18  {}.mkv'

for subdir, dirs, files in walk('.'):
    onlyfiles = [f for f in listdir(subdir) if isfile(join(subdir, f) )]
    onlyfiles = [f for f in onlyfiles if f.endswith(".avi")]
    if not onlyfiles:
        continue


    params = ""
    for file in sorted(onlyfiles):
        params += file + "|"

    new_file_name = subdir[2:] # Удаляем "./"
    new_file_name = "../raw/" + new_file_name # Добавляем каталог
    new_file_name = new_file_name.replace(" ", "").replace("(", r"\(").replace(")", r"\)")
    # Если уже есть такой, пропускаем
    if (isfile(new_file_name[3:]+".mkv")):
        continue
    command = template_command.format(params, new_file_name)
    print(command)
    chdir(subdir)
    system(command)
    chdir("..")
