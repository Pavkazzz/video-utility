import os
import subprocess
import platform
from multiprocessing import Pool
import progressbar


class Media:
    bar = progressbar.ProgressBar(max_value=progressbar.UnknownLength)

    def __init__(self, name, file_path):
        self.filePath = file_path
        self.name = name
        self.platform = platform.system()
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

    def calculate_length(self):
        if self.platform == "Linux":
            command = 'ffprobe -i  "' + self.filePath + '" 2>&1 |grep "Duration"'
        elif self.platform == "Windows":
            command = 'ffprobe.exe -i  "' + self.filePath + '" 2>&1 |findstr "Duration"'
        else:
            raise Exception("this platform is not supported")
        a = str(subprocess.check_output(command, shell=True))
        del command
        a = a.split(",")[0].split("Duration:")[1].strip()
        try:
            self.hours, self.minutes, self.seconds = a.split(':')
        except ValueError:
            self.hours, self.minutes, self.seconds = 0, 0, 0

        return self


def get_async(item):
    num = item[0]
    Media.bar.update(num)
    item = item[1]
    val = item.calculate_length()
    return val


if __name__ == "__main__":
    directory = "Z:\\Tapes\\raw"
    files = os.listdir(directory)
    fileList = []
    pool = Pool(5)
    for num, file in enumerate(files):
        fileList.append([num, Media(file, os.path.join(directory, file))])
    Media.bar.max_value = len(files)
    fileList = pool.map(get_async, fileList)

    media = {}

    for file in fileList:
        name = file.name
        media[name] = [[file.hours, file.minutes, file.seconds],
                       float(str(file.hours) + str(file.minutes) + str(file.seconds))
                       ]
    sorted_by_value = sorted(media.items(), key=lambda kv: kv[1][1])
    Media.bar.finish()
    for element in sorted_by_value:
        print(f"{element[0]} - {element[1][0][0]}:{element[1][0][1]}:{element[1][0][2]}")

    input()
