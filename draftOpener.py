import json
import random
import requests
import os

# This file as a whole is extremely badly made tbh
# To "Done" do: Save the set info locally after first prompt and extract from that instead of querying every time
# To "Done" do: Make exception for when query is called with no internet/database down
# To "Done" do: Make the 1 button catch up feature
# TO"meh"DOLP: Weighted randomization somehow
# To "Done in banlistmaker.py" do: Banlist file
# To"Done"do: Receive YDK file return banlist file option? Make this a new module
# TO"Temporarily Disabled"DO: Remove/Rework SepFoils and its usages
# TO"Done"DO: Change IO manipulation instances to use info from config
import packviewer

common = []
short = []
sshort = []
rare = []
super = []
ultra = []
ulti = []
secret = []
ghost = []
starlight = []
goldrare = []
coreSets = ["Legend of Blue Eyes White Dragon", "Metal Raiders", "Spell Ruler", "Pharaoh's Servant",
            "Labyrinth of Nightmare", "Legacy of Darkness", "Pharaonic Guardian", "Magician's Force",
            "Dark Crisis", "Invasion of Chaos", "Ancient Sanctuary", "Soul of the Duelist",
            "Rise of Destiny", "Flaming Eternity", "The Lost Millennium", "Cybernetic Revolution",
            "Elemental Energy", "Shadow of Infinity", "Enemy of Justice", "Power of the Duelist",
            "Cyberdark Impact", "Strike of Neos", "Force of the Breaker", "Tactical Evolution",
            "Gladiator's Assault", "Phantom Darkness", "Light of Destruction", "The Duelist Genesis",
            "Crossroads of Chaos", "Crimson Crisis", "Raging Battle", "Ancient Prophecy",
            "Stardust Overdrive", "Absolute Powerforce", "The Shining Darkness", "Duelist Revolution",
            "Storm of Ragnarok", "Extreme Victory", "Generation Force", "Photon Shockwave",
            "Order of Chaos", "Galactic Overlord", "Return of the Duelist", "Abyss Rising",
            "Cosmo Blazer", "Lord of the Tachyon Galaxy", "Judgment of the Light", "Shadow Specters",
            "Legacy of the Valiant", "Primal Origin", "Duelist Alliance", "The New Challengers",
            "Secrets of Eternity", "Crossed Souls", "Clash of Rebellions", "Dimension of Chaos",
            "Breakers of Shadow", "Shining Victories", "The Dark Illusion", "Invasion: Vengeance",
            "Raging Tempest", "Maximum Crisis", "Code of the Duelist", "Circuit Break",
            "Extreme Force", "Flames of Destruction", "Cybernetic Horizon", "Soul Fusion",
            "Savage Strike", "Dark Neostorm", "Rising Rampage", "Chaos Impact",
            "Ignition Assault", "Eternity Code", "Rise of the Duelist", "Phantom Rage",
            "Blazing Vortex", "Lightning Overdrive", "Dawn of Majesty", "Burst of Destiny",
            "Battle of Chaos"
            ]

reprintSets = ["Dark Beginning 1", "Dark Beginning 2", "Dark Revelation Volume 1",
               "Dark Revelation Volume 2", "Dark Revelation Volume 3", "Dark Revelation Volume 4"]

battleSets = ["Battle Pack: Epic Dawn", "Battle Pack 2: War of the Giants", "War of the Giants Reinforcements",
              "War of the Giants: Round 2", "Battle Pack 3: Monster League"]

buildSets = ["The Secret Forces", "High-Speed Riders""Wing Raiders", "Destiny Soldiers", "Fusion Enforcers",
             "Spirit Warriors", "Dark Saviors", "Hidden Summoners", "The Infinity Chasers", "Mystic Fighters",
             "Secret Slayers", "Genesis Impact", "Ancient Guardians", "The Grand Creators"]

collectionSets = ["Number Hunters", "Dragons of Legend", "Dragons of Legend 2", "Dragons of Legend: Unleashed",
                  "Battles of Legend: Light's Revenge", "Battles of Legend: Relentless Revenge",
                  "Battles of Legend: Hero's Revenge", "Battles of Legend: Armageddon", "Brothers of Legend"]

duelistSets = ["Duelist Pack Collection Tin 2008", "Duelist Pack Collection Tin 2009",
               "Duelist Pack Collection Tin 2010", "Duelist Pack Collection Tin 2011",
               "Duelist Pack Collection Tin: Jaden Yuki", "Duelist Pack: Aster Phoenix",
               "Duelist Pack: Battle City", "Duelist Pack: Chazz Princeton",
               "Duelist Pack: Crow", "Duelist Pack: Dimensional Guardians", "Duelist Pack: Jaden Yuki",
               "Duelist Pack: Jaden Yuki 2", "Duelist Pack: Jaden Yuki 3", "Duelist Pack: Jesse Anderson",
               "Duelist Pack: Kaiba", "Duelist Pack: Rivals of the Pharaoh", "Duelist Pack: Special Edition",
               "Duelist Pack: Yugi", "Duelist Pack: Yusei", "Duelist Pack: Yusei 2", "Duelist Pack: Yusei 3",
               "Duelist Pack: Zane Truesdale", "Legendary Duelists", "Legendary Duelists: Ancient Millennium",
               "Legendary Duelists: Immortal Destiny", "Legendary Duelists: Magical Hero",
               "Legendary Duelists: Rage of Ra", "Legendary Duelists: Season 1", "Legendary Duelists: Season 2",
               "Legendary Duelists: Sisters of the Rose", "Legendary Duelists: White Dragon Abyss"
               ]

goldSets = ["Gold Series", "Gold Series 2009", "Gold Series 3", "Gold Series 4: Pyramids Edition",
            "Gold Series: Haunted Mine"]

hiddenArset = ["Hidden Arsenal", "Hidden Arsenal 2", "Hidden Arsenal 3", "Hidden Arsenal 4: Trishula's Triumph",
               "Hidden Arsenal 5: Steelswarm Invasion", "Hidden Arsenal 5: Steelswarm Invasion: Special Edition",
               "Hidden Arsenal 6: Omega Xyz", "Hidden Arsenal 7: Knight of Stars", "Hidden Arsenal: Special Edition",
               ]

collectorBoxSets = ["Duelist Saga", "Duel Power", "Duel Overload"]

sixtySets = ["Pendulum Evolution", "Shadows in Valhalla", "Fists of the Gadgets", "Toon Chaos", "King's Court"]

otherSets = ["Ghosts From the Past", "Millenium Pack", "World Superstars"]
# uniques: Ghosts From the Past, Millenium Pack, World Superstars
# demo decks: meh

retropack = ["Retro Pack", "Retro Pack 2"]

draftSets = ["Legend of Blue Eyes White Dragon", "Metal Raiders", "Spell Ruler", "Pharaoh's Servant",
             "Labyrinth of Nightmare", "Legacy of Darkness", "Pharaonic Guardian", "Magician's Force",
             "Dark Crisis", "Invasion of Chaos", "Ancient Sanctuary", "Soul of the Duelist",
             "Rise of Destiny", "Flaming Eternity", "The Lost Millennium", "Cybernetic Revolution",
             "Elemental Energy", "Shadow of Infinity", "Enemy of Justice", "Power of the Duelist",
             "Cyberdark Impact", "Strike of Neos", "Force of the Breaker", "Tactical Evolution",
             "Gladiator's Assault", "Phantom Darkness", "Light of Destruction", "The Duelist Genesis",
             "Crossroads of Chaos", "Crimson Crisis", "Raging Battle", "Ancient Prophecy",
             "Stardust Overdrive", "Dark Beginning 1", "Dark Beginning 2", "Dark Revelation Volume 1",
             "Dark Revelation Volume 2", "Dark Revelation Volume 3", "Dark Revelation Volume 4",
             "Hidden Arsenal", "Gold Series", "Dark Legends", "Retro Pack", "Gold Series 2009",
             "Retro Pack 2"]

debug = False


def randCard(rarity):
    """
    Returns a random card from the assigned rarity
    :param rarity: List, contains all cards of a certain rarity in the pack
    :return: Dict, ImportantInfo dict, params = "name", "id", "rarity", "type"
    """
    return rarity[random.randint(-1, len(rarity) - 1)]


def setup(packName, packN, boxRatio, visuals, pulldir):
    """
    Pulls packN amoutn of packs from packName
    Also checks if the json containing the data isn't already present within the files
    TO"Meh"DO: Split this function into multiples
    :param packName: String, name of the pack, must be present within the YGOprodeck database
    :param packN: Int, amount of packs to pull
    :param boxRatio: Boolean, whether the pack should conform to box ratios or not
    :return: packlist: A list containing all the packs pulled in order
    """
    hasSshort = False
    superRate = 0
    ultraRate = 0
    secretRate = 0
    hasUltimate = False
    hasSecret = True
    hasGhost = False
    gHolo = False
    hasStarlight = False
    packlist = []
    reprint = False
    if (os.path.isdir('./packinfo') and os.path.isfile('./packinfo/' + packName.replace(" ", "") + '.json')):
        print("Found deck json within files")
    else:
        print("Creating json for deck")
        base_url = "https://db.ygoprodeck.com/api/v7/cardinfo.php"
        site = "?cardset=" + packName
        random.seed()

        try:
            first_response = requests.get(base_url + site, timeout=5)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection and pack not in files. Aborting")
            return
        response_list = first_response.json()

        # print(first_response.json())

        if ("error" in response_list):
            print("Invalid pack")
            return

        with open('./packinfo/' + packName.replace(" ", "") + '.json', "w") as f:
            json.dump(response_list, f)

        print("\n\n")

    jsonReady = None
    with open('./packinfo/' + packName.replace(" ", "") + '.json', "r") as f:
        jsonReady = json.load(f)
        # print(jsonReady)
    data = jsonReady["data"]
    sequence = []
    if packName in coreSets:
        sequence = ["C", "C", "C", "C", "C", "C", "C", "R", "F"]
        if packName in coreSets[
                       coreSets.index("Legend of Blue Eyes White Dragon"):coreSets.index("Light of Destruction")]:
            sequence = ["C", "C", "C", "C", "C", "C", "C", "RF", "C"]
        else:
            sequence = ["C", "C", "C", "C", "C", "C", "C", "R", "F"]

        if packName in coreSets[
                       coreSets.index("Legend of Blue Eyes White Dragon"):coreSets.index("Soul of the Duelist")]:
            superRate = 6
            ultraRate = 12
            secretRate = 31
            if packName in coreSets[
                           coreSets.index("Legend of Blue Eyes White Dragon"):coreSets.index("Legacy of Darkness")]:
                hasSshort = True
                print("This pack has super short prints")
        elif packName in coreSets[coreSets.index("Soul of the Duelist"):coreSets.index("Tactical Evolution")]:
            superRate = 6
            ultraRate = 24
            secretRate = 31
            hasUltimate = True
            print("This pack has 1:24 Ultras")
            print("This pack has Ultimates")
            if packName in coreSets[coreSets.index("Soul of the Duelist"):coreSets.index("Strike of Neos")]:
                hasSecret = False
                print("This pack has no Secret Rares")
        elif packName in coreSets[coreSets.index("Tactical Evolution"):coreSets.index("Breakers of Shadow")]:
            superRate = 5
            ultraRate = 12
            secretRate = 31
            hasUltimate = True
            hasGhost = True
            print("This pack has Ghost Rares")
            print("This pack has 1:5 Supers")
            print("This pack has Ultimates")
            if packName in coreSets[coreSets.index("The Shining Darkness"):coreSets.index("Breakers of Shadow")]:
                secretRate = 23
                print("This pack has 1:23 Secrets")
        elif packName in coreSets[coreSets.index("Breakers of Shadow"):]:
            gHolo = True
            ultraRate = 6
            secretRate = 12
            sequence[8] = "SF"
            print("This pack has guaranteed Holos every pack")
            print("This pack has 1:6 Ultras")
            print("This pack has 1:12 Secrets")
            if packName in coreSets[coreSets.index("Rising Rampage"):]:
                print("This pack has Starlight rares")
                hasStarlight = True
                if packName in coreSets[coreSets.index("Eternity Code"):]:
                    print("This pack has no Rare cards")
                    sequence[7] = "C"
    elif packName in reprintSets:
        sequence = ["CM", "CM", "CM", "CM", "CM", "CM", "CS", "CS", "CS", "CT", "CT", "CT"]
        reprint = True
        ultraRate = 12
        superRate = 6
    elif packName in hiddenArset:
        sequence = ["SR", "SR", "SR", "SR", "SCR"]
    elif packName in goldSets:
        sequence = ["C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C", "C",
                    "C", "C", "GR", "GR", "GR"]
    elif packName in retropack:
        superRate = 5
        ultraRate = 12
        secretRate = 23
        sequence = ["C", "C", "C", "C", "C", "C", "C", "R", "F"]
    elif packName == "Dark Legends":
        superRate = 5
        ultraRate = 12
        secretRate = 23
        sequence = ["C", "C", "C", "C", "C", "C", "C", "R", "F", "C", "C", "C"]
    localSetup(data, packName, visuals)

    if (debug):
        printInfoSetup()

    if (boxRatio and packName in coreSets):

        superOk = False
        ultraOk = False
        secretOk = False

        boxModSuper = 0
        boxModUltra = 0
        boxModSecret = 0

        superMod = random.randint(0, superRate)
        if (superMod == 0):
            boxModSuper += 1
        elif (superMod == superRate-1):
            boxModSuper -= 1

        ultraMod = random.randint(0, ultraRate)
        if (ultraMod == 0):
            boxModUltra += 1
        elif (ultraMod == ultraRate-1):
            boxModUltra -= 1

        secretMod = random.randint(0, secretRate)
        if (secretMod == 0):
            boxModSecret += 1
        elif (secretMod == secretRate-1):
            boxModSecret -= 1

        while not(superOk and ultraOk and secretOk):
            cardlist = []
            packlist = []
            for i in range(0, packN):
                packlist.append(openPack(hasSshort, ultraRate, superRate, secretRate, hasUltimate, hasSecret,
                                         hasGhost, hasStarlight, sequence, reprint))
            for pack in packlist:
                for card in pack:
                    cardlist.append(card)
            foils = foilCount(cardlist, False, packName, packN, True, False, pulldir)
            superOk = gHolo or len(foils["Super Rare"]) == int(packN / superRate) + boxModSuper
            ultraOk = len(foils["Ultra Rare"]) == int(packN / ultraRate) + boxModUltra
            #print(len(foils["Ultra Rare"]))
            #print(int(packN / ultraRate) + boxModUltra)
            secretOk = not hasSecret or secretRate > 24 or len(foils["Secret Rare"]) == int(
                packN / secretRate) + boxModSecret

    else:
        for i in range(0, packN):
            packlist.append(openPack(hasSshort, ultraRate, superRate, secretRate, hasUltimate, hasSecret,
                                     hasGhost, hasStarlight, sequence, reprint))
    return packlist


def reprintClean(pack):
    """
    Helper function specifically for reprint packs.
    :param pack: List, contains the 12 cards in a pack
    :return: temppack, the pack with the higher rarity cards implanted in
    """
    temppack = pack
    rarity = random.randint(0, 12)
    if rarity == 0:
        card = randCard(ultra)
        if ("Monster" in card["type"]):
            temppack[5] = card
        elif ("Spell" in card["type"]):
            temppack[8] = card
        elif ("Trap" in card["type"]):
            temppack[11] = card
    else:
        rarity = random.randint(0, 6)
        if rarity == 0:
            card = randCard(super)
            if ("Monster" in card["type"]):
                temppack[5] = card
            elif ("Spell" in card["type"]):
                temppack[8] = card
            elif ("Trap" in card["type"]):
                temppack[11] = card

            card = randCard(rare)
            if ("Monster" in card["type"]):
                temppack[4] = card
            elif ("Spell" in card["type"]):
                temppack[7] = card
            elif ("Trap" in card["type"]):
                temppack[10] = card
        else:
            card = randCard(rare)
            if ("Monster" in card["type"]):
                temppack[4] = card
            elif ("Spell" in card["type"]):
                temppack[7] = card
            elif ("Trap" in card["type"]):
                temppack[10] = card
    return temppack


def localSetup(data, packName, visuals):
    """
    Sets up the global lists with the cards from their respective rarities
    :param data: Output from the database
    :param packName: String, the pack's exact name
    """
    for card in data:
        for cardset in card["card_sets"]:

            importantInfo = {
                "name": card["name"],
                "id": card["id"],
                "rarity": "",
                "type": card["type"]
            }
            if (visuals):
                importantInfo['image'] = 'https://storage.googleapis.com/ygoprodeck.com/pics_small/' + str(
                    card["id"]) + '.jpg'

            if (cardset["set_name"] == packName and cardset["set_rarity"] == "Common"):
                importantInfo["rarity"] = "Common"
                common.append(importantInfo) if importantInfo not in common else None

            elif (cardset["set_name"] == packName and cardset["set_rarity"] == "Short Print"):
                importantInfo["rarity"] = "Short Print"
                short.append(importantInfo) if importantInfo not in short else None

            elif (cardset["set_name"] == packName and cardset["set_rarity"] == "Super Short Print"):
                importantInfo["rarity"] = "Super Short Print"
                sshort.append(importantInfo) if importantInfo not in sshort else None

            elif (cardset["set_name"] == packName and cardset["set_rarity"] == "Rare"):
                importantInfo["rarity"] = "Rare"
                rare.append(importantInfo) if importantInfo not in rare else None

            elif (cardset["set_name"] == packName and cardset["set_rarity"] == "Super Rare"):
                importantInfo["rarity"] = "Super Rare"
                super.append(importantInfo) if importantInfo not in super else None

            elif (cardset["set_name"] == packName and cardset["set_rarity"] == "Ultra Rare"):
                importantInfo["rarity"] = "Ultra Rare"
                ultra.append(importantInfo) if importantInfo not in ultra else None

            elif (cardset["set_name"] == packName and cardset["set_rarity"] == "Secret Rare"):
                importantInfo["rarity"] = "Secret Rare"
                secret.append(importantInfo) if importantInfo not in secret else None

            if (cardset["set_name"] == packName and cardset["set_rarity"] == "Ultimate Rare"):
                importantInfo["rarity"] = "Ultimate Rare"
                ulti.append(importantInfo) if importantInfo not in ulti else None

            if (cardset["set_name"] == packName and cardset["set_rarity"] == "Ghost Rare"):
                importantInfo["rarity"] = "Ghost Rare"
                ghost.append(importantInfo) if importantInfo not in ghost else None

            if (cardset["set_name"] == packName and cardset["set_rarity"] == "Starlight Rare"):
                importantInfo["rarity"] = "Starlight Rare"
                starlight.append(importantInfo) if importantInfo not in starlight else None

            if (cardset["set_name"] == packName and cardset["set_rarity"] == "Gold Rare"):
                importantInfo["rarity"] = "Gold Rare"
                goldrare.append(importantInfo) if importantInfo not in goldrare else None


def openPack(hasSshort, ultraRate, superRate, secretRate, hasUltimate, hasSecret, hasGhost, hasStarlight,
             sequence, reprint):
    """
    Opens a single pack from a designated set
    :param hasSshort: Boolean, whether the pack contains Super Short Prints. (Those are mostly present in old sets)
    :param ultraRate: Int, The chances of pulling an Ultra Rare in that particular pack
    :param superRate: Int, The chances of pulling an Super Rare in that particular pack
    :param secretRate: Int, The chances of pulling an Secret Rare in that particular pack
    :param hasUltimate: Boolean, whether the pack contains Ultimate Rares.
    :param hasSecret: Boolean, whether the pack contains Secret Rares.
    :param hasGhost: Boolean, whether the pack contains Ghosts.
    :param hasStarlight: Boolean, whether the pack contains Starlight Rares.
    :param sequence: List, has the cards in sequence
    :param reprint: Boolean, whether the pack is a reprint sets
    :return: pack: List, list of the cards that were pulled
    """
    pack = []
    for r in sequence:
        if (r == "C"):
            srarity = random.randint(0, 30 + len(short))
            if (hasSshort and len(sshort) != 0 and srarity == 0):
                pack.append(randCard(sshort))
            elif (len(short) != 0 and (srarity == 1 or srarity == 2)):
                pack.append(randCard(short))
            else:
                pack.append(randCard(common))
        elif (r == "R"):
            pack.append(randCard(rare))
        elif (r == "F" or r == "SF" or r == "RF"):
            pulled = False
            if hasStarlight and not pulled:
                rarity = random.randint(0, 576)
                if (rarity == 0):
                    pack.append(randCard(starlight))
                    pulled = True

            if hasGhost and not pulled:
                rarity = random.randint(0, 288)
                if (rarity == 0):
                    pack.append(randCard(ghost))
                    pulled = True

            if hasUltimate and not pulled:
                rarity = random.randint(0, 32)
                if (rarity == 0):
                    pack.append(randCard(ulti))
                    pulled = True

            if hasSecret and not pulled:
                rarity = random.randint(0, secretRate)
                if (rarity == 0):
                    pack.append(randCard(secret))
                    pulled = True

            rarity = random.randint(0, ultraRate)
            if rarity == 0 and not pulled:
                pack.append(randCard(ultra))
                pulled = True

            if (not pulled):
                if r == "SF":
                    pack.append(randCard(super))
                else:
                    rarity = random.randint(0, superRate)
                    if (rarity == 0):
                        pack.append(randCard(super))
                    else:
                        if r == "RF":
                            pack.append(randCard(rare))
                        else:
                            srarity = random.randint(0, 60)
                            if (len(sshort) != 0 and srarity == 1):
                                pack.append(randCard(sshort))
                            elif (len(short) != 0 and (srarity == 2 or srarity == 3)):
                                pack.append(randCard(short))
                            else:
                                pack.append(randCard(common))


        elif r == "CM":
            card = randCard(common)
            while (not "Monster" in card["type"]):
                card = randCard(common)
            pack.append(card)
        elif r == "CS":
            card = randCard(common)
            while (not "Spell" in card["type"]):
                card = randCard(common)
            pack.append(card)
        elif r == "CT":
            card = randCard(common)
            while (not "Trap" in card["type"]):
                card = randCard(common)
            pack.append(card)
        elif r == "SR":
            pack.append(randCard(super))
        elif r == "SCR":
            pack.append(randCard(secret))
        elif r == "GR":
            pack.append(randCard(goldrare))
    if (reprint):
        pack = reprintClean(pack)
    return pack


def foilPrint(list, rarityName):
    """
    Prints all the cards pulled from a given rarity
    :param list: The rarity list from which to pull from
    :param rarityName: The displayed name upon printing
    """
    if (len(list) > 0):
        print("You pulled " + str(len(list)) + " " + rarityName + "(s): ")
        for card in list:
            if (list[len(list) - 1] == card):
                print(card["name"])
            else:
                print(card["name"], end=", ")


def foilCount(cardlist, sepFoils, packName, packNumber, boxRatio, printInfo, pulldir):
    """
    Counts the amount of foil cards opened.
    :param cardlist: List, a list with all cards pulled
    :param sepFoils: Boolean, whether to put the foils in a different YDK or not
    :param packName: String, name of the pack for printing purpose
    :param packNumber: Int, needed for sepFoils, number of packs pulled
    :param boxRatio: Boolean, whether box ratios are in effect or not
    :param printInfo: :Boolean, whether to print the extra info or not
    :return foils, a list containing the result:
    """
    mySuper = []
    myUltra = []
    myShort = []
    mySShort = []
    myUltimate = []
    mySecret = []
    myGhost = []
    myStarlight = []
    for card in cardlist:
        if (card["rarity"] == "Short Print"):
            myShort.append(card)
        elif (card["rarity"] == "Super Rare"):
            mySuper.append(card)
        elif (card["rarity"] == "Ultra Rare"):
            myUltra.append(card)
        elif (card["rarity"] == "Super Short Print"):
            mySShort.append(card)
        elif (card["rarity"] == "Secret Rare"):
            mySecret.append(card)
        elif (card["rarity"] == "Ghost Rare"):
            myGhost.append(card)
        elif (card["rarity"] == "Starlight Rare"):
            myStarlight.append(card)

    if (sepFoils):
        foilYdk(mySuper, myUltra, myUltimate, mySecret, myGhost, myStarlight, packName, packNumber, pulldir)

    if (printInfo):
        foilPrint(myShort, "Normal Rare")
        foilPrint(mySShort, "Super Short Print")
        foilPrint(mySuper, "Super Rare")
        foilPrint(myUltra, "Ultra Rare")
        foilPrint(myUltimate, "Ultimate Rare")
        foilPrint(mySecret, "Secret Rare")
        foilPrint(myGhost, "Ghost Rare")
        foilPrint(myStarlight, "Starlight Rare")

    if (boxRatio):
        foils = {
            "Super Rare": mySuper,
            "Ultra Rare": myUltra,
            "Secret Rare": mySecret
        }
        return foils


def foilYdk(mySuper, myUltra, myUltimate, mySecret, myGhost, myStarlight, packName, packNumber, pulldir):
    """
    Transforms the pulled cards into a .ydk file
    :param mySuper: List, cards of said rarity
    :param myUltra: List, cards of said rarity
    :param myUltimate: List, cards of said rarity
    :param mySecret: List, cards of said rarity
    :param myGhost: List, cards of said rarity
    :param myStarlight: List, cards of said rarity
    :param packName: String, name of the pack
    :param packNumber: Int, number of packs pulled
    :return:
    """
    if os.path.isdir(pulldir):
        if os.path.isfile(pulldir + '/' + packName.replace(" ", "") + '_' + str(packNumber) + "packsDraftFoils.ydk"):
            print("Foils file already found. Aborting")
            return
        with open(pulldir + '/' + packName.replace(" ", "") + '_' + str(packNumber) + "packsDraftFoils.ydk", "x") as f:
            f.write("#Made with Iason PackOpener Foils Only File\n")
            f.write("#main\n")
            for card in myStarlight:
                f.write(str(card["id"]) + "\n")
            for card in myGhost:
                f.write(str(card["id"]) + "\n")
            for card in mySecret:
                f.write(str(card["id"]) + "\n")
            for card in myUltimate:
                f.write(str(card["id"]) + "\n")
            for card in myUltra:
                f.write(str(card["id"]) + "\n")
            for card in mySuper:
                f.write(str(card["id"]) + "\n")
            f.close()


def printInfoSetup():
    """
    Debugging function to print all cards pulled of each rarity.
    """
    print(common)
    print(len(common))
    print(short)
    print(len(short))
    print(sshort)
    print(len(sshort))
    print(rare)
    print(len(rare))
    print(super)
    print(len(super))
    print(ultra)
    print(len(ultra))
    print(secret)
    print(len(secret))
    print(ulti)
    print(len(ulti))
    print(ghost)
    print(len(ghost))
    print(starlight)
    print(len(starlight))


def main(toOpen, howmany, writeYdk, trimYdk, writeFoil, ratio, visuals, printInfo, pulldir):
    """
    :param toOpen: String, pack to open
    :param howmany: Int, how many packs
    :param writeYdk: Boolean, wheter there should be a ydk output or not
    :param trimYdk: Boolean, should copies above 3 be ignored
    :param writeFoil: Boolean, should foils be separated
    :param ratio: Boolean, should it adhere to box ratios?
    """
    write = writeYdk
    trim = trimYdk
    cardlist = []
    countFoils = True
    sepFoils = False
    boxRatio = ratio
    #print("HERE: " + toOpen)

    packName = "Stardust Overdrive"
    packNumber = 24

    if (len(toOpen) != 0):
        packName = toOpen
    if (howmany != 0):
        packNumber = howmany

    if (not packName in coreSets):
        sepFoils = False

    packlist = setup(packName, packNumber, boxRatio, visuals, pulldir)

    if write:
        if os.path.isdir(pulldir):
            if os.path.isfile(pulldir + '/' + packName + "Draft.ydk") or \
                    os.path.isfile(
                        pulldir + '/' + packName + "DraftTrimmed.ydk"):
                print("Found deck pulls within files already. Aborting write")
                write = False
            else:
                if (trim):
                    f = open(
                        pulldir + '/' + packName + "DraftTrimmed.ydk",
                        "x")
                else:
                    f = open(pulldir + '/' + packName + "Draft.ydk", "x")
                f.write("#Made with IasonPackOpener\n")
                f.write("#main\n")
        else:
            print("Invalid pull directory. Aborting")
            return

    for pack in packlist:
        if(printInfo):
            print("Opening one pack of " + packName)

        for card in pack:
            if(printInfo):
                print(card)
            cardlist.append(card)

            if write:
                if (trim):
                    if (cardlist.count(card) < 4):
                        f.write(str(card["id"]) + " - " + card["name"] + "\n")
                else:
                    f.write(str(card["id"]) + " - " + card["name"] + "\n")

    if (countFoils):
        foilCount(cardlist, sepFoils, packName, packNumber, False, printInfo, pulldir)
    if (visuals):
        packviewer.main(packlist)
    cleanup(packlist, cardlist)


def cleanup(packlist, cardlist):
    """
    Cleans up each global list
    :param packlist:
    :param cardlist:
    """
    #print("Cleaning")
    global common
    common = []
    global short
    short = []
    global sshort
    sshort = []
    global rare
    rare = []
    global super
    super = []
    global ultra
    ultra = []
    global ulti
    ulti = []
    global secret
    secret = []
    global ghost
    ghost = []
    global starlight
    starlight = []
    global goldrare
    goldrare = []


if __name__ == '__main__':
    main("Tactical Evolution", 0, False, False, False, False, False, False, './')
