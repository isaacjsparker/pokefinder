#import libraries
import requests
from bs4 import BeautifulSoup

#get regional locations
page = requests.get('https://bulbapedia.bulbagarden.net/wiki/Region')
soup = BeautifulSoup(page.text, 'html.parser')
regions = soup.findAll("table")
region_links = regions[3].tr.td.nextSibling.nextSibling.findAll('a')

for each in region_links:
    #get locations
    region_url = 'https://bulbapedia.bulbagarden.net' + each.get('href')
    print (each.get('href')[6:])
    page = requests.get(region_url)
    soup = BeautifulSoup(page.text, 'html.parser')
    poke_place_list_list = soup.findAll("table")
    poke_places = poke_place_list_list[len(poke_place_list_list)-2]
    poke_places_items = poke_places.findAll('a')

    #get pokemon at each location
    for each in poke_places_items:
        location_url = 'https://bulbapedia.bulbagarden.net' + each.get('href')
        #TODO add other test pages
        #test case for pokemon forms
        #location_url = 'https://bulbapedia.bulbagarden.net/wiki/Striaton_City'
        #test case for allies column:
        #location_url = 'https://bulbapedia.bulbagarden.net/wiki/Poni_Meadow'
        print ("   ",each.get('href')[6:])
        page = requests.get(location_url)
        soup = BeautifulSoup(page.text, 'html.parser')        
            
        place_poke_list = soup.find('span', {'id' : 'Pok.C3.A9mon'})

        try:
            for each in place_poke_list:
                looper = each.parent.parent.nextSibling.nextSibling
                while (not looper.name == 'h2') :
                    if looper.name == 'table':
                        for child in looper.children:
                            #sun and moon do not work, likely because of new allies column, if statement appears to be broken
                            if (child.name == 'tr' and child.get("style") == "text-align:center;"):
                                #individual pokemon level
                                #name
                                poke_data = child.children
                                poke_name = child.td.table.tr.td
                                poke_counter = 0
                                for each in poke_data:
                                    if (poke_counter == 1):
                                        ifFirst = True
                                        for child in poke_name.children:
                                            try:
                                                for each in child.span.children:
                                                    if ifFirst:
                                                        print ("      ",each)
                                                        ifFirst = False
                                                    else:
                                                        print ("         ",each)
                                            except AttributeError:
                                                pass
                                    elif (each.name == "th" and each.a):
                                        #differentiate "S" for Silver version and "S" for Sapphire version
                                        if(each.a.string == "S"):
                                            if(each.a.get("href") == "/wiki/Pok%C3%A9mon_Gold_and_Silver_Versions"):
                                                print ("          Si")
                                            elif(each.a.get("href") == "/wiki/Pok%C3%A9mon_Ruby_and_Sapphire_Versions"):
                                                print ("          Sa")
                                            elif(each.a.get("href") == "/wiki/Pok%C3%A9mon_Sun_and_Moon"):
                                                print ("          Su")
                                            else:
                                                #TODO throw uncaught "S" region error
                                                print ("          S")
                                        elif(each.a.string == "R"):
                                        else:
                                            print ("         ",each.a.string)
                                    poke_counter += 1                               
                    looper = looper.nextSibling       
        except TypeError:
            print ("       No pokemon here")
