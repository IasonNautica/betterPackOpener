import os
import PySimpleGUI as sg

import animeCards


def main(d, banlistfolder, banlistname, whitelist):
    """
    Makes a banlist file using the dictionary created from one of the helper functions
    :param d: Dict
    :param banlistname: String, The name of the new file
    :param whitelist: Boolean, Whether the banlist is a whitelist or not.
    """

    text = sg.popup_get_text("Please insert the desired output file's name. (Cancel for default name)", "Filename")
    if(text != "" and text != None):
        banlistname = text
    if (whitelist and (text == "" or text == None)):
        banlistname = "Whitelist" + banlistname
    if os.path.isdir(banlistfolder):
        try:
            with open(banlistfolder + '/' + banlistname + ".lflist.CONF", "x") as f:
                f.write("#[" + banlistname + "]" + "\n")
                f.write("!" + banlistname + "\n")
                if (whitelist):
                    f.write("$whitelist\n")
                for key, value in d.items():
                    f.write(key + " " + str(value[1]) + " -" + value[0] + "\n")

                if (whitelist):
                    # Removing extra cards
                    samenamecards = ["295517", "22702055", "26534688", "74335036", "34103656", "2819435", "91932350", "27927359",
                                     "54415063", "80316585"]

                    animeexclusive = animeCards.animecards

                    rushexclusive = ["160406009", "160003011", "160406001", "160406002", "160003010", "160001011",
                                     "160003008", "160004011", "160002004", "160003007", "160003006", "160003005",
                                     "160002014", "160406006", "160002040", "160002041", "160002044", "160201011",
                                     "160201001", "160406010", "160411002", "160003052", "160003053", "160005054",
                                     "160002050", ]

                    for code in samenamecards:
                        if not code in d:
                            f.write(code + " -1 - " + "umiclone" + "\n")
                    for code in animeexclusive:
                        if not code in d:
                            f.write(str(code) + " -1 - " + "anime card" + "\n")
                    for code in rushexclusive:
                        if not code in d:
                             f.write(code + " -1 - " + "rush card" + "\n")
            sg.popup("All done!\nSaved " + banlistname + ".lflist.CONF \nto\n" + banlistfolder)

        except FileExistsError:
            sg.popup("Error, file already exists. Aborting write")
            print("Error, file already exists. Aborting write")
