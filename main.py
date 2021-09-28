#!/usr/bin/python3
import os
import traceback

import banydkappend
import draftOpener
import banlistmaker
import whitelistmaker
import banlistappend

import PySimpleGUI as sg

# TO"Done"DO: Figure out why popups keep closing the program
# TO"Done"DO: Implement sets checkbox in uitest.py
# TO"Done"DO: Include the banlist maker (or just make it standalone)
# TO"Done"DO: Dont actually need an action for checkboxes
# TO"Done"DO: Config Menu
# TO"Kinda done"DO: Implement Config file
# TO"Done"DO: Refactor those fucking filenames
# TO"Meh"DO: Check for random empty spaces...
# TO"Done"DO: Whitelist flag select in -TMERGEBL-
# TO"Done"DO: Implement dictolist in banydkappend.py and banlistmaker.py
# TO"Done"DO: Figure out why sets window is crashing: Bad refactor
# TO"Was done already"DO: Give the newest window focus when opened
# TO"DoneDO: Add "quit" button to visual pack opener
# TO"Done"DO: Exceptions for every error
# TO"Done"DO: Disable input screen while set selection screen is up
# TO"Done"DO: Popup "Done" and close window after Saving on config menu
# TO"Can't do this"DO: Disable writing in the output box
# TO"Done"DO: Let user select pack amount
pulldir = ""
bandir = ""
SYMBOL_UP = '▲'
SYMBOL_DOWN = '▼'


def showpack(pack):
    for card, n in enumerate(pack):
        pass


def pullMultiple(packs, writeYdk, trimYdk, writeFoil, ratio, visuals, printInfo, packamount):
    """
    runs draftOpener.main multiple times, depending on the kind of set pulled
    Gold Series = 5 Packs
    Hidden Arsenal = 8 Packs
    Everything Else = 24 packs
    :param packs: List, list of the packs to be opened in a row
    :param writeYdk: Boolean, should it write a YDK or not
    :param trimYdk: Boolean
    :param writeFoil: Boolean
    :param ratio: Boolean
    """
    getConfigInfo()
    howmany = 0
    if(packamount=="Default"):
        for pack in packs:
            if pack in draftOpener.goldSets:
                howmany = 5
            elif pack in draftOpener.hiddenArset:
                howmany = 8
            else:
                howmany = 24
            draftOpener.main(pack, howmany, writeYdk, trimYdk, writeFoil, ratio, visuals, printInfo, pulldir)
    else:
        for pack in packs:
            draftOpener.main(pack, packamount, writeYdk, trimYdk, writeFoil, ratio, visuals, printInfo, pulldir)

def createChecks(layoutmod, sets, setsname, core):
    """
    Creates the layout for the selectable list of sets
    :param layoutmod: List, the layout file to be modified
    :param sets: List, the list of sets to be added to the layout
    :param setsname: String, display name for the list of sets
    :param core: Boolean, whether it's a core set or not (changes the acronym slightly)
    :return:
    """
    n = len(layoutmod) + 1
    c = 0
    layoutmod.append([sg.Text(setsname)])
    layoutmod.append([])
    for item in sets:
        c += 1
        split = item.split(" ")
        acro = ""
        for i in split:
            if (core):
                if len(i) > 3:
                    acro += i[0] + i[1]
            else:
                acro += i[0]
        layoutmod[n].append(sg.Checkbox(acro, enable_events=True, key=item, tooltip=item))
        # print(item + " : " + acro)
        if (c == 10):
            n += 1
            layoutmod.append([])
            c = 0

    return layoutmod


def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=False), shrink=True)


def makeToolsWindow():
    getConfigInfo()
    section1 = [  # [sg.Checkbox('Folder Select', enable_events=True, key='-FFSWITCH-', tooltip=tip)],
        [sg.In(), sg.FilesBrowse(file_types=(("YDK Files", "*.ydk"),), key="-S1FILE-", initial_folder=pulldir)],
        # [sg.In(), sg.FolderBrowse(key="-S1FOLDER-", initial_folder='./',disabled=False)],
        # [sg.Input(key='-IN11-')],
        [sg.Button('Go', button_color=('black', 'green'), key='-TMAKEWL-')]]

    tip = "Whether it's a whitelist or not."
    section2 = [[sg.Checkbox('Whitelist', enable_events=True, key='-S2CHECK-', tooltip=tip)],
                [sg.In(),
                 sg.FileBrowse(file_types=(("Banlist Files", "*.CONF"),), key="-S2FILE1-", initial_folder=bandir)],
                [sg.In(),
                 sg.FileBrowse(file_types=(("Banlist Files", "*.CONF"),), key="-S2FILE2-", initial_folder=bandir)],
                [sg.B('Go', button_color=('black', 'green'), key='-TMERGEBL-')]]

    section3 = [[sg.Combo(('Banned', 'Limited', 'Semi'), default_value='Banned', key='-S3BMFLAG-', readonly=True)],
                [sg.In(), sg.FileBrowse(file_types=(("YDK Files", "*.ydk"),), key="-S3FILE-", initial_folder=pulldir)],
                [sg.B('Go', button_color=('black', 'Green'), key='-TMAKEBL-')]]

    section4 = [[sg.Checkbox('Whitelist', enable_events=True, key='-S4CHECK-', tooltip=tip)],
                [sg.In(),
                 sg.FileBrowse(file_types=(("Banlist Files", "*.CONF"),), key="-S4FILE1-", initial_folder=bandir)],
                [sg.In(), sg.FileBrowse(file_types=(("YDK Files", "*.ydk"),), key="-S4FILE2-", initial_folder=pulldir)],
                [sg.B('Go', button_color=('black', 'Green'), key='-TAPPENDWL-')]]

    tip1 = "Choose one or more YDK files and merge them together in one whitelist"
    tip2 = "Merge two banlists. The second one has priority over the other"
    tip3 = "Creates a banlist from a YDK. Each card in the YDK will be set to the dropdown menu's value"
    tip4 = "Appends a .ydk to a whitelist. Useful for adding your new pulls to your main whitelist file"

    layout = [[sg.Text('Select the desired function below:')],
              #### Section 1 part ####
              [sg.T(SYMBOL_UP, enable_events=True, k='-TOPENCOLL-1-', text_color='black', tooltip=tip1),
               sg.T('Create Whitelist', enable_events=True, text_color='black', k='-TOPENCOLL-1-TEXT', tooltip=tip1)],
              [collapse(section1, '-SEC1-')],
              [sg.T("------------------------------------------------")],
              #### Section 2 part ####
              [sg.T(SYMBOL_UP, enable_events=True, k='-TOPENCOLL-2-', text_color='black', tooltip=tip2),
               sg.T('Banlist Merger', enable_events=True, text_color='black', k='-TOPENCOLL-2-TEXT', tooltip=tip2)],
              [collapse(section2, '-SEC2-')],
              [sg.T("------------------------------------------------")],
              #### Section 3 part ####
              [sg.T(SYMBOL_UP, enable_events=True, k='-TOPENCOLL-3-', text_color='black', tooltip=tip3),
               sg.T('Banlist Maker', enable_events=True, text_color='black', k='-TOPENCOLL-3-TEXT', tooltip=tip3)],
              [collapse(section3, '-SEC3-')],
              [sg.T("------------------------------------------------")],
              #### Section 4 part ####
              [sg.T(SYMBOL_UP, enable_events=True, k='-TOPENCOLL-4-', text_color='black', tooltip=tip4),
               sg.T('Banlist Append', enable_events=True, text_color='black', k='-TOPENCOLL-4-TEXT', tooltip=tip4)],
              [collapse(section4, '-SEC4-')],
              [sg.T("------------------------------------------------")],
              [sg.Button('Exit')]]

    return sg.Window('Tools', layout, finalize=True)


def makeSetWindow():
    """
    Creates a layout file with all the sets available as globals.
    Basically just executes createChecks multiple times in a row
    :return: sg.Window
    """
    layout = []
    createChecks(layout, draftOpener.coreSets, "Core Sets", True)
    createChecks(layout, draftOpener.reprintSets, "Reprint Sets", False)
    createChecks(layout, draftOpener.hiddenArset, "Hidden Arsenal", False)
    createChecks(layout, draftOpener.retropack, "Retro packs", False)
    layout.insert(0, [
        [sg.Button('Select All', key='-SALL-'), sg.Button('Select None', key='-SNONE-'),
         sg.Button('Catch up to draft', key='-SDRAFT-'), sg.Button('Exit', key='-SEXIT-')]])

    return sg.Window('Sets', layout, finalize=True, location=(0, 50), disable_close=True)


def makeConfigWindow():
    """
    Creates the window for the configuration file
    :return: sg.Window
    """
    layoutConfig = [
        [sg.Text("Pulls Folder   "), sg.Input(key="-CPULLFOLDER-", change_submits=True, default_text=pulldir),
         sg.FolderBrowse(key="-CPULLBROWSER-")],
        [sg.Text("Banlist Folder"), sg.Input(key="-CBANFOLDER-", change_submits=True, default_text=bandir),
         sg.FolderBrowse(key="-CBANBROWSER-")],
        [sg.Button("Save", key="-CSAVE-")]
    ]
    return sg.Window('Configuration', layoutConfig, finalize=True)


def makeMainWindow():
    """
    Creates the main UI screen
    :return: sg.Window
    """

    ydkmess = "Pulled packs will be put in a YDK file inside ./pulls."
    remextmess = "Doesn't add any copies of the card to the YDK after you have acquired 3"
    sepfoilmess = "Adds the foil pulls to a different YDK file also inside ./pulls"
    boxratmess = "Makes the box adhere to common box ratios, with a small RNG"
    visualmess = "Graphically shows your pulls"
    printmess = "Prints the pulls to the window below"
    layout = [[sg.Text('Please type the set to be pulled below:')],
              ###Checkboxes
              [sg.Checkbox('YDK Output', tooltip=ydkmess, enable_events=True, key="-YDKOUT-"),
               sg.Checkbox('Remove Extras', tooltip=remextmess, disabled=True, enable_events=True, key="-REMEXTRA-"),
               sg.Checkbox('Separate Foils', tooltip=sepfoilmess, disabled=True, enable_events=True, key="-SEPFOIL-",
                           visible=False),
               sg.Checkbox('Box Ratios', tooltip=boxratmess, enable_events=True, key="-BOXRAT-"),
               sg.Checkbox('Visuals', tooltip=visualmess, enable_events=True, key="-VISPULLS-"),
               sg.Checkbox('Print pulls', tooltip=printmess, enable_events=True, key="-PRINTPULLS-", default=True),

               sg.T("Pack Amount:"),
               sg.Combo(["Default", 5, 6, 7, 8, 9, 10, 15, 20, 24, 29, 30, 36], default_value="Default", key="-PACKAMOUNT-", readonly=True)],

              ###CheckBoxes
              [sg.In(key='-IN-')],

              [sg.Button('Go', key='-GO-'), sg.Button('Clear', key='-CLEAR-'), sg.Button('Exit', key='-EXIT-')],
              [sg.Button('Select Sets', key='-SETLAUNCHER-'), sg.Button('Configure Folders', key='-CONFIGLAUNCHER-'),
               sg.Button('Whitelist/Banlist Tools', key='-TOOLSLAUNCHER-')],

              [sg.Multiline(size=(100, 20), key='-OUTPUT-', reroute_stdout=True, autoscroll=True)]
              ]
    return sg.Window('Pack Opener', layout, finalize=True, resizable=True)


def getConfigInfo():
    global pulldir
    global bandir
    if os.path.isdir('./config'):
        if os.path.isfile('./config/info.txt'):
            with open('./config/info.txt', 'r') as f:
                lines = f.read().splitlines()
                s1 = lines[0].split(" ")
                s2 = lines[1].split(" ")
                pulldir = s1[1]
                bandir = s2[1]

    else:
        os.makedirs('./config')


def main():
    """
    Main event loop. Renders the UI elements and handles the inputs
    """
    writeYdk = False
    trimYdk = False
    writeFoil = False
    ratio = False
    sg.theme("Dark Blue")

    opened1, opened2, opened3, opened4 = False, False, False, False

    mainWindow = makeMainWindow()
    setsWindow = None
    configWindow = None
    toolsWindow = None

    try:
        while True:  # Event Loop
            window, event, values = sg.read_all_windows()

            if event in (sg.WIN_CLOSED, '-EXIT-', '-SEXIT-', '-CEXIT-'):
                window.close()
                if window == setsWindow:  # if closing win 2 or 3, mark as closed
                    setsWindow = None
                elif window == configWindow:
                    configWindow = None
                elif window == toolsWindow:
                    toolsWindow = None
                elif window == mainWindow:  # if closing win 1, exit program
                    break

            # Main Menu  ----

            elif event == '-GO-':
                getConfigInfo()
                print(values['-IN-'])
                if values[
                    '-IN-'] in draftOpener.coreSets + draftOpener.reprintSets + draftOpener.battleSets + draftOpener.buildSets + draftOpener.collectionSets + draftOpener.duelistSets + draftOpener.goldSets + draftOpener.hiddenArset + draftOpener.collectorBoxSets + draftOpener.sixtySets + draftOpener.otherSets + draftOpener.retropack:

                    pullMultiple([values['-IN-']], window['-YDKOUT-'].get(), window['-REMEXTRA-'].get(),
                                 window['-SEPFOIL-'].get(), window['-BOXRAT-'].get(), window['-VISPULLS-'].get(),
                                 window['-PRINTPULLS-'].get(), values['-PACKAMOUNT-'])
                    window['-IN-'].update('')


                elif setsWindow:
                    print("Pulling according to selection")
                    topull = []
                    for e in setsWindow.element_list():
                        if isinstance(e, sg.Checkbox):
                            if e.get() == True:
                                topull.append(e.Tooltip)
                    pullMultiple(topull, window['-YDKOUT-'].get(), window['-REMEXTRA-'].get(), window['-SEPFOIL-'].get(),
                                 window['-BOXRAT-'].get(), window['-VISPULLS-'].get(), window['-PRINTPULLS-'].get(),
                                 values['-PACKAMOUNT-'])

                else:
                    print("Invalid output")

            elif event == '-CLEAR-':
                window['-OUTPUT-'].update('')

            elif event == "-YDKOUT-":
                if window['-REMEXTRA-'].get():
                    window['-REMEXTRA-'].update(False)
                if window['-SEPFOIL-'].get():
                    window['-SEPFOIL-'].update(False)
                window['-REMEXTRA-'].update(disabled=not window['-YDKOUT-'].get())
                window['-SEPFOIL-'].update(disabled=not window['-YDKOUT-'].get())

            elif event == '-CONFIGLAUNCHER-' and not configWindow:
                getConfigInfo()
                configWindow = makeConfigWindow()

            elif event == '-SETLAUNCHER-' and not setsWindow:
                setsWindow = makeSetWindow()
                window['-IN-'].update(disabled=True)

            elif event == '-TOOLSLAUNCHER-' and not toolsWindow:
                toolsWindow = makeToolsWindow()

            # Set Menu     ----

            elif event == '-SALL-':
                for e in setsWindow.element_list():
                    if isinstance(e, sg.Checkbox):
                        e.update(value=True)

            elif event == '-SNONE-':
                for e in setsWindow.element_list():
                    if isinstance(e, sg.Checkbox):
                        e.update(value=False)

            elif event == '-SDRAFT-':
                for e in setsWindow.element_list():
                    if isinstance(e, sg.Checkbox):
                        if e.Tooltip in draftOpener.draftSets:
                            e.update(value=True)

            # Config Menu ----

            elif event == '-CSAVE-':
                getConfigInfo()
                print("New ban folder: " + values['-CBANFOLDER-'])
                print("New pulls folder: " + values['-CPULLFOLDER-'])
                with open("./config/info.txt", 'w+') as f:
                    f.write("PFolder: " + values['-CPULLFOLDER-'] + " \n")
                    f.write("BFolder: " + values['-CBANFOLDER-'] + " \n")
                sg.popup("Done!")
                configWindow = False
                window.close()

            # Tools Menu ----

            if event == '-TOPENCOLL-1-':
                opened1 = not opened1
                window['-TOPENCOLL-1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
                window['-SEC1-'].update(visible=opened1)

            if event == '-TOPENCOLL-2-':
                opened2 = not opened2
                window['-TOPENCOLL-2-'].update(SYMBOL_DOWN if opened2 else SYMBOL_UP)
                window['-SEC2-'].update(visible=opened2)

            if event == '-TOPENCOLL-3-':
                opened3 = not opened3
                window['-TOPENCOLL-3-'].update(SYMBOL_DOWN if opened3 else SYMBOL_UP)
                window['-SEC3-'].update(visible=opened3)

            if event == '-TOPENCOLL-4-':
                opened4 = not opened4
                window['-TOPENCOLL-4-'].update(SYMBOL_DOWN if opened4 else SYMBOL_UP)
                window['-SEC4-'].update(visible=opened4)

            if event == '-TMAKEWL-':
                getConfigInfo()
                # print(values['-S1FILE-'])
                files = values['-S1FILE-'].split(';')
                # print(files)
                # print(bandir)
                if (values['-S1FILE-'] != ''):
                    message = whitelistmaker.main(files, bandir)
                    sg.popup("All done!\nSaved " + message)
                else:
                    sg.popup("Error, invalid path")

            if event == '-TMERGEBL-':
                # print(values['-S2FILE1-'])
                # print(values['-S2FILE2-'])

                getConfigInfo()
                if (os.path.isfile(values['-S2FILE1-']) and os.path.isfile(values['-S2FILE2-'])):
                    message = banlistappend.main(values['-S2FILE1-'], values['-S2FILE2-'], window['-S2CHECK-'].get(), bandir)
                    sg.popup("All done!\n Saved " + message)
                else:
                    sg.popup("Error, invalid path")

            if event == '-TMAKEBL-':
                # print(values['-S3FILE-'])
                # print(values['-S3BMFLAG-'])

                getConfigInfo()
                if (os.path.isfile(values['-S3FILE-'])):
                    message = banlistmaker.main(bandir, values['-S3FILE-'], values['-S3BMFLAG-'])
                    sg.popup("All done!\n Saved " + message)
                else:
                    sg.popup("Error, invalid path")

            if event == '-TAPPENDWL-':
                # print(values['-S4FILE1-'])
                # print(values['-S4FILE2-'])

                getConfigInfo()
                if (os.path.isfile(values['-S4FILE1-']) and os.path.isfile(values['-S4FILE2-'])):
                    message = banydkappend.main(values['-S4FILE1-'], values['-S4FILE2-'], window['-S4CHECK-'].get(), bandir)
                    sg.popup("All done!\n Saved " + message)
                else:
                    sg.popup("Error, invalid path")
    except Exception as e:
        tb = traceback.format_exc()
        sg.popup_error(f'AN EXCEPTION OCCURRED!', e, tb)

if __name__ == '__main__':
    main()
