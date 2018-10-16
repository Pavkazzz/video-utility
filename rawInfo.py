import os
import subprocess
import platform
from multiprocessing import Pool
import progressbar


def getLength(file):
    filepath = file[1]
    name = file[0]
    if platform.system() == "Linux":
        command = 'ffprobe -i  "' + filepath + '" 2>&1 |grep "Duration"'
    elif platform.system() == "Windows":
        command = 'ffprobe.exe -i  "' + filepath + '" 2>&1 |findstr "Duration"'

    else:
        raise Exception("this platform is not supported")
    a = str(subprocess.check_output(command, shell=True))
    del command
    a = a.split(",")[0].split("Duration:")[1].strip()

    try:
        h, m, s = a.split(':')
        return name, h, m, s
    except ValueError:
        return name, 0, 0, 0


if __name__ == "__main__":
    directory = "raw"
    files = os.listdir(directory)
    pool = Pool(4)
    filePool = [[file, os.path.join(directory, file)] for file in files]
    poolResult = pool.map(getLength, filePool)
    media = {}
    for file in poolResult:
        name = file[0]
        h = file[1]
        m = file[2]
        s = file[3]
        media[name] = [[h, m, s], float(str(h) + str(m) + str(s))]
    sorted_by_value = sorted(media.items(), key=lambda kv: kv[1][1])
    for element in sorted_by_value:
        print(f"{element[0]} - {element[1][0][0]}:{element[1][0][1]}:{element[1][0][2]}")
