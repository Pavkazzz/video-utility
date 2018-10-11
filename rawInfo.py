import os
import subprocess


def getLength(filename):
    a = str(subprocess.check_output('ffprobe -i  "' + filename + '" 2>&1 |findstr "Duration"', shell=True))
    a = a.split(",")[0].split("Duration:")[1].strip()
    try:
        h, m, s = a.split(':')
        return h, m, s
    except ValueError:
        return 0, 0, 0


if __name__ == "__main__":
    directory = "raw/"
    files = os.listdir(directory)
    value = 0
    media = {}
    mediaStr = {}
    for file in files:
        value += 1
        filePath = directory+file
        h, m, s = getLength(filePath)
        media[file] = [h, m, s]
        mediaStr[file] = float(str(h) + str(m) + str(s))
    sorted_by_value = sorted(mediaStr.items(), key=lambda kv: kv[1])
    for element in sorted_by_value:
        print(element[0] + " - " +
              str(media[element[0]][0]) + ":" + str(media[element[0]][1]) + ":" + str(media[element[0]][2]))
