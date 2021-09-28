import os

def main(d, banlistfolder, banlistname, whitelist):
    """
    Makes a banlist file using the dictionary created from one of the previous 2 helper functions
    (Those being buildRestrict and buildWhitelist)
    :param d: Dict, the aforementioned dictionary
    :param banlistname: String, The name of the new file
    :param whitelist: Boolean, Whether the banlist is a whitelist or not.
    """
    if(whitelist):
        banlistname = "Whitelist" + banlistname
    if os.path.isdir(banlistfolder):
        try:
            with open(banlistfolder + '/' + banlistname + ".lflist.CONF", "x") as f:
                f.write("#[" + banlistname + "]" + "\n")
                f.write("!"+ banlistname + "\n")
                if(whitelist):
                    f.write("$whitelist\n")
                for key, value in d.items():
                    f.write(key + " " + str(value[1]) + " -" + value[0] + "\n")
        except FileExistsError:
            print("Error, file already exists. Aborting print")