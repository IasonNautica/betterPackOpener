import os
import dictolist
import ntpath

#TO"Done"DO: Let user select YDK folder and files for banned/limit/semi
#TO"Done"DO: Append mode
#TO"Done: Technically implemented with AppendMode" DO: Individual YDK option for draft mode
#TO"Meh"DO: Add enum for the flag in buildRestrict

def buildRestrict(file, flag):
    """
    Given a .ydk file, builds a banlist file using its contents
    :param flag: String, "banned", "limited" or "semi". Each card will be set to this flag's corresponding value (0, 1, 2)
    :param file: String, filepath to the .ydk
    :return d: Dict, A dictionary containing all this info
    """
    d = {}
    restrict = 3
    if flag == "Banned":
        restrict = 0
    elif flag == "Limited":
        restrict = 1
    elif flag == "Semi":
        restrict = 2

    with open(file) as f:
        for line in f:
            if not line.startswith(('#', '!', 'ï»¿')):
                split = line.split(" ", 1)
                if not split[0].strip() in d:
                    if (len(split) == 2):
                        d[split[0].strip()] = (split[1].rstrip(), restrict)
                    else:
                        print("here")
                        d[split[0].strip()] = ("", restrict)
    return d


def main(banlistFolder, banlistYDK, flag ):
    """
    :param banlistFolder: String, filepath to the folder with the banlists
    :param banlistYDK: String, filepath to the .ydk base file for the banlist
    :param banlistName: String, name of the new banlist file
    """
    d = buildRestrict(banlistYDK, flag)
    dictolist.main(d, banlistFolder, ntpath.basename(banlistYDK) + "banlist", False)
    return ntpath.basename(banlistYDK) + "banlist\nto\n" + banlistFolder


if __name__ == '__main__':
    main()
