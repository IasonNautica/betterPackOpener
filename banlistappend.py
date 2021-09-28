import os
import ntpath

import dictolist


def main(list1, list2, whitelist, bandir):
    """
    Merges two banlist files. List2 will take precedence over list1
    :param list1: Base banlist filepath
    :param list2: second Banlist filepath. Its bans will take priority over banlist1
    :param whitelist: Boolean, whether the banlist is a whitelist or not.
    """
    d = {}
    if (os.path.isfile(list1) and os.path.isfile(list2)):
        with open(list1, 'r') as wfile:
            for line in wfile:
                if not line.startswith(('#', '!', 'ï»¿', '$')):
                    v = line.split(" ", 2)
                    #print(v)
                    d[v[0]] = ("", (v[1]))

        with open(list2, 'r') as yfile:
            for line in yfile:
                if not line.startswith(('#', '!', 'ï»¿', '$')):
                    v = line.split(" ", 2)
                    if v[0] in d.keys():
                        d[v[0]] = ("", (v[1]))
                    else:
                        if not whitelist:
                            d[v[0]] = ("",(v[1]))

    dictolist.main(d, bandir, ntpath.basename(list1) + ntpath.basename(list2) + "-Merged", whitelist)
    return ntpath.basename(list1) + ntpath.basename(list2) + "-Merged\nto\n" + bandir


if __name__ == '__main__':
    main("./banlist/4mepulls(useformetagaminglater).lflist.CONF", "./banlist/draft_baselist.lflist.CONF",
         "./test/DraftPulls9212012.lflist.CONF", True)
