# betterPackOpener
A Yugioh pack opening alternative made in Python. 
The main reason why I made this was to have a more accurate pack opener, the most popular one has lots of mistakes and doesn't work as it should. The other reason was to have a pack opener that lets you open 24 packs as if they were a box and not stray packs.

## Table of contents
* [Features](#features)
* [Technologies](#technologies)
* [Download](#download)
* [User Guide](#userguide)

## Features
Pull cards from any of the included sets either as stray packs or as a box.
YDK output containing all your files.
(WIP) Visual opener using card images from the internet.
Create an Edopro whitelist using a YDK file
Merge banlist function
Make an edopro banlist using a YDK file (Not actually related to pack opening)
Append a banlist/whitelist (Useful for adding cards to a banlist file)

## Technologies
The UI was made with pythonSimpleGui.
Pretty much all card information is pulled directly from Ygoprodeck's database.

## Download
Get the lastest version at the [release page](https://github.com/IasonNautica/betterPackOpener/releases/tag/v1.0)
Linux users should download the source code and compile/run it themselves.

## User Guide
Though I've tried to make the tooltips and titles fairly self explanatory, here follows a small user guide on how to use this program:
![Main Screen](https://imgur.com/phlqmpP.png)
**Checkboxes:**

YDK Output - If checked, prints the files as a YDK file readable by DuelingBook/Edopro/etc in the desired Pulls directory

Remove Extras -  Only available if YDK Output is checked, removes any copies of a card after the third one from the YDK

Box Ratios - Pull as if pulling from a box instead of stray packs (Basically "guarantees" a certain amount of Super/Ultra/Secret Rares depending on the ratios the set has. Only works in core sets)

Visuals: Show your pulls one by one in a graphical interface.

Print pulls: On by default, prints cards to the output window.

Pack Amount: On the default settings, pulls 24 packs for every set, except Gold Series sets (5) and Hidden Arsenal sets (8)

**Go**: Type a sets' name and select Go to pull it (Alternatively, you can select them from a list if clicking **Select Sets**).

![Select Sets Screen](https://imgur.com/pBgud5i.png)
**Select Sets:**
Check whichever sets you want to pull and then click Go on the main window. This disables writing down the pack's name. Be sure not to close the second window if you want to pull from a selection.
Catch up to draft option should be a few weeks off, so beware.

![Configure Screen](https://imgur.com/NhVMiOr.png)
Where to save your banlists (.lflist.CONF) and pulls (.ydk) files. By default, should point to the current directory's /pulls and /banlist, but not a bad idea to double check this.

![Tools](https://imgur.com/6PK4z5R.png)
**Create Whitelist**: Select one or more ydk files to create a whitelist from. You can use this to create a whitelist fine for Edopro, allowing easy management and deck building. If you want to export this to Edopro, put it in the /repositories/lflists inside Project Ignis' directory.

**Banlist Merger**: Select two .lflist.CONF files to merge. If both of them are hitting the same card, the second one's hit will be preferred over the first.

**Banlist Maker**: Used for creating custom banlists for tourneys and such. You can select a .ydk file and it will produce a banlist putting all that YDK's cards to the selected restriction. You can append this into the current TCG banlist using the previous function.

**Banlist Append**:
Appends a .ydk file to a banlist one. This is useful for adding some newly pulled cards to your main banlist file. If doing so, don't forget to check the Whitelist box.
