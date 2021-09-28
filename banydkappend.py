import ntpath
import os

import dictolist


def main(banlist, ydk, whitelist, dir):
    """
    Merges a banlist file with a ydk.
    :param banlist: String, filepath to the banlist.lflist.CONF file
    :param ydk: String, filepath to the .ydk file
    :param whitelist: boolean
    :param dir String, the banlist folder directory
    """
    d = {}
    if (os.path.isfile(banlist) and os.path.isfile(ydk)):
        with open(ydk) as f:
            for line in f:
                if not line.startswith(('#', '!', '$', 'ï»¿')):
                    # print(d)
                    split = line.split(" ", 2)
                    # print(split)

                    t = None
                    if len(split) > 2:
                        t = split[2]
                    else:
                        t = ""

                    if split[0].strip() in d.keys():
                        # print("yes")
                        # print(d[split[0].strip()][1])
                        if d[split[0].strip()][1] != 3:
                            d[split[0].strip()] = (d[split[0].strip()][0], d[split[0].strip()][1] + 1)
                    else:
                        d[split[0].strip()] = (t.strip('\n'), 1)
        with open(banlist, 'r') as wfile:
            for line in wfile:
                if not line.startswith(('#', '!', 'ï»¿', '$')):
                    v = line.split(" ", 2)
                    # print(v)
                    t = None
                    if len(v) > 2:
                        t = v[2]
                    else:
                        t = ""
                    if int(v[1]) == 0:
                        d[v[0]] = (t.strip('\n'), int(v[1]))
                    else:
                        if v[0] in d.keys():
                            if int(d[split[0].strip()][1]) > int(v[1]):
                                d[split[0].strip()] = (d[split[0].strip()][0], v[1])

    dictolist.main(d, dir, ntpath.basename(banlist) + ntpath.basename(ydk) + "-Merged", whitelist)
    return ntpath.basename(banlist) + ntpath.basename(ydk) + "-Merged\nto\n" + dir


if __name__ == '__main__':
    main('C:/Users/literallyme/Desktop/Yugioh-Pack-Opening-Simulator-master/banlist/draft_baselist.lflist.CONF',
         'C:/Users/literallyme/Desktop/Yugioh-Pack-Opening-Simulator-master/pulls/RetroPack_24packsDraft.ydk', True,
         'C:/Users/literallyme/Desktop/Yugioh-Pack-Opening-Simulator-master/banlist')
