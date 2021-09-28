
import os
from datetime import datetime
from os import listdir
from os.path import isfile
from os.path import splitext


import dictolist


def buildWhitelist(inp):
    """
    :param inp: A list of YDK paths
    :return: A dictionary mapping each card ID to how many copies were found, maxes at 3.
    """
    d = {}
    for file in inp:
        with open(file) as f:
            for line in f:
                if not line.startswith(('#', '!', '$', 'ï»¿')):
                    # print(d)
                    split = line.split(" ", 1)
                    if split[0].strip() in d:
                        if (d[split[0].strip()][1] != 3):
                            d[split[0].strip()] = (d[split[0].strip()][0], d[split[0].strip()][1] + 1)
                    else:
                        if (len(split) == 2):
                            d[split[0].strip()] = (split[1].rstrip(), 1)
                        else:
                            d[split[0].strip()] = ("", 1)
    return d


def main(inp, banlistF):
    """
    Builds a .lflist.CONF file using file from a YDK data.
    :param inp: A list of YDK files, a folder containing YDKS or the filepath to a YDK file
    :param banlistF: The folder where the banlists are located
    :param whitelistN: The name of the returning folder
    :return String, message to be show inside the popup in the main UI
    """
    d = {}
    if isinstance(inp, list):
        d = buildWhitelist(inp)
    elif os.path.isfile(inp):
        d = buildWhitelist([inp])
    elif os.path.isdir(inp):
        l = []
        for file in listdir(inp):
            fname = inp + '/' + file
            print(fname)
            if isfile(fname):
                ext = splitext(file)[-1].lower()
                if ext == ".ydk":
                    l.append(fname)
        d = buildWhitelist(l)
    else:
        print("ERROR whitelistmaker.py: Invalid input")
        return

    now = datetime.now()

    current_time = now.strftime("%H%M%S")
    print(banlistF)
    dictolist.main(d, banlistF, current_time + "-MergedList", True)
    return current_time + "-MergedList.lflist\n to\n " + banlistF


if __name__ == '__main__':
    main(["./pulls/4mepulls(useformetagaminglater).ydk"], "./banlist", "4mepulls(useformetagaminglater)")
