from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
import time
import os
BaseLibUrl = "https://maplelegends.com/lib/monster?page="
EndLibUrl = "&search=&filter=1&order=2&sort=1"
BaseMobUrl = "https://maplelegends.com/lib/monster?id="
BaseMobImage = "https://maplelegends.com/static/images/lib/monster/"
ImagesPath = "images"
page = ""
MonsterID = 0
MonsterName = ""
MonsterLevel = 0
MonsterHP = 0
MonsterAvoid = 0
MonsterWeak = [False] * 5
MonsterStrong = [False] * 5
MonsterImmune = [False] * 5
MAX_PAGES = 1   # 127
MonsterLocations = [False] * 14  # Maple Island, Victoria Island, Orbis/ElNath,Aqua, Ludi/Omega/KFT/Ellin, Mu Lung/Herb Town, Ariant/Magatia, Leafre/ToT, Zipangu, NT, China, Thailand, Taiwan, Singapore,PQ, Manual

def extract_tag(source, StartTag, EndTag):
    StartIndex = source.find(StartTag) + len(StartTag)
    EndIndex = source[StartIndex:].find(EndTag)
    return source[StartIndex:StartIndex + EndIndex]


def element_checker(element):
    array = [False] * 5
    for string in element:
        if string.strip() == "Ice":
            array[0] = True
        elif string.strip() == "Lightning":
            array[1] = True
        elif string.strip() == "Fire":
            array[2] = True
        elif string.strip() == "Poison":
            array[3] = True
        elif string.strip() == "Holy":
            array[4] = True
    return array


for i in range(MAX_PAGES):  # This section goes through each page of the library
    try:
        page = urlopen(BaseLibUrl + str(i + 1) + EndLibUrl)  # goes through each page
        html = page.read().decode("utf-8")
    except HTTPError:
        print("Error on page " + str(i+1))
    table_index = html.find("class=\"table text-center table-bordered\">")  # the index of the actual table
    html = html[table_index+len("class=\"table text-center table-bordered\">"):]
    MOB_PER_PAGE = int(html.count("<a href=") / 2)  # There are two instances of an a tag per html file (image and text)
    for j in range(1):  # Go through each mob found
        # time.sleep(10)  # don't forget to uncomment this jackass
        IDStartindex = html.find("<a href=\"/lib/monster?id=") + len("<a href=\"/lib/monster?id=")
        MonsterID = extract_tag(html,"<a href=\"/lib/monster?id=","\">")  # gets the mobid
        html = html[html.find("</center>"):]
        # this section for getting mob name
        MonsterName = extract_tag(html, "<a href=\"/lib/monster?id=" + str(MonsterID) + "\">", "</a>")
        print(MonsterName)
        print(MonsterID)
        # access mob page here
        try:
            MobPage = urlopen("https://maplelegends.com/lib/monster?id=0100100&tab=2")  # &tab=2 refers to drops or locations
            Mobhtml = MobPage.read().decode("utf-8")
            # Now we grab the picture of the mob
            # FullPath = os.path.join(ImagesPath, MonsterID + ".png")
            # urlretrieve("https://maplelegends.com/static/images/lib/monster/" + MonsterID,FullPath)
            # ## For future reference: we can copy paste below if we need other stats
            # Find its level
            MonsterLevel = extract_tag(Mobhtml, "Level: ", "</td>")
            # Find its avoid
            MonsterAvoid = extract_tag(Mobhtml, "Avoidability: ", "</td>")
            # Find its weaknesses
            Weak = extract_tag(Mobhtml, "Weak:", "</p>").split(',')
            MonsterWeak = element_checker(Weak)
            # Find its strong against
            Strong = extract_tag(Mobhtml, "Strong:", "</p>").split(',')
            MonsterStrong = element_checker(Strong)
            # Find its immunity
            Immune = extract_tag(Mobhtml, "Immune:", "</p>").split(',')
            MonsterImmune = element_checker(Immune)
            # Oh boy now we go see how many maps this thing is in
            MapCount = Mobhtml.count("/lib/map?id=")
            if MapCount == 0:
                MonsterLocations[13] = True #  If it doesn't have any maps listed, just review it manually
            else:
                Mobhtml = Mobhtml[Mobhtml.find("/lib/map?id="):]
                for k in range(MapCount):
                    WorldID = extract_tag(Mobhtml, "/lib/map?id=", "\">")  # Find the Map ID

                    Mobhtml = Mobhtml[Mobhtml.find("</a>"):]  # We need to leave this tag to avoid refinding the same thing
                    Mobhtml = Mobhtml[Mobhtml.find("/lib/map?id="):]  # Find the next instance of a map id
            # Finish with all mob info, now we add it all to json
        except HTTPError:
            print("Error opening monster id: " + str(MonsterID))
        html = html[IDStartindex:]  # shift to next mob
        NextIndex = html.find("<center>")
        html = html[NextIndex + len("<center>"):]  # truncates so we can find next instance of a mob

    time.sleep(10)  # to be nice and kind to kimmy's server, we wait 10 seconds before moving on to the next page
