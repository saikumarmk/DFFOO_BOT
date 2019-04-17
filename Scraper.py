from selenium import webdriver
from bs4 import BeautifulSoup
import json
import time


LOCALE = "JP"
ROOT = "https://dissidiadb.com"
CHARPAGE = "/characters"

browser=webdriver.Firefox()


def bs_parse(url,locale=LOCALE):
    browser.get(url)
    if locale == "JP":
        browser.find_element_by_xpath("//span[@title='Japan']").click()
    #browser.find_element_by_xpath("//span[@title='Global']")
    html = browser.page_source
    return BeautifulSoup(html, 'lxml')


# Retrieve Page Name
def retrieveNames():    
    charpage = bs_parse(ROOT+CHARPAGE)
    lst= charpage.body.div.main.div.ul    

    charnames = [l.find("span",{"class":"name"}).string for l in lst] # use this for their name
    charurl = [l.find("a",{"class":"imageLink"})['href'][1:] for l in lst]
    CHARACTERS = dict(zip(charnames,charurl))
    CHARACTERS["Cecil (DK)"] = "cecil"
    CHARACTERS.pop("Cecil (Dark Knight)")

    with open('dependencies/{}/charnames.json'.format(LOCALE),'w') as u:
        json.dump(CHARACTERS,u)


# Dumps Character Info
def getCharacter(charName):
    soup = bs_parse(ROOT+"/"+charName)
    
    # Retrieve Crystal Type and Weapon type
    crystal = soup.find("span",{"class":"icon crystal"})['title']
    weapon = soup.find("p",{"class":"weapon-type"}).find("span",{"class":"icon"})['title']

    # Retrieve Name
    name = soup.find("h2",{"class":"header"}).string

    # Retrieve Picture URL
    picture = soup.find("img",{"class":"artwork_image"})['src']
    pictureurl = ROOT+picture

    # Retrieve Stats
    table = soup.find("div",{"class":"stats"}).table
    table_body = table.find('tbody')
    stats = {}
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        nams = row.find_all('th')
        cols = [ele.text.strip() for ele in cols]
        stats[nams[0]['title']] = [ele for ele in cols if ele] # Get rid of empty values

    # Retrieve Command Abilities
    table = soup.find("div",{"class":"abilities"}).table
    table_body = table.find('tbody')
    commands = {}
    rows = table_body.find_all('tr')

    for row in rows:
        # Annoying issue here, if the attack has an elemental attribute
        # Then it's the second span
        # If not, then it's the first span
        # We fix this by checking if there exists a span with class="small icon"
        cols = row.find('td',{"class":"ability"}).find_all("div")[0].text
        icons = set(row.find('td',{"class":"description"}).find_all("div")[0].find_all("span","small icon"))
        allspans = set(row.find('td',{"class":"description"}).find_all("div")[0].find_all("span"))
        nm = allspans - icons
        nmn = nm.pop()
        #nams = row.find('td',{"class":"description"}).find_all("span")[1].text
        ltx = " ".join([n if type(n)==type(nmn.contents[0]) else "" for n in nmn.contents])
        commands[cols] = ltx # Get rid of empty values


    # Retrieve Passive Abilities
    table = soup.find("div",{"class":"passives"}).table
    table_body = table.find('tbody')
    passives = {}
    rows = table_body.find_all('tr')
    for row in rows:
        comb = row.find_all('td')
        n = comb[0].find_all('div')[0].text
        e = comb[1].find_all('div')[0].text
        passives[n] = e.encode("ascii", "replace").decode().replace("?"," ") # Get rid of empty values


    # Retrieve Artifact passives list
    '''
    table = soup.find("div",{"class":"artifacts"}).table # this is undefined for some reason

    table_body = table.find('tbody') # error here
    artifacts = {}
    rows = table_body.find_all('tr')
    cutrows = []
 
    for i in range(0,len(rows),2):
        cutrows.append([rows[i],rows[i+1]])
        
    for row in cutrows:
        
        n = row[0].find("td",{"class":"passive"}).find_all("div")[0].text
        effect = row[1].find('td',{"class":"effect max"}).text
        artifacts[n] = effect.encode("ascii", "replace").decode().replace("?"," ") # Get rid of empty values
    '''

    # Retrieve Weapons
    table = soup.find("div",{"class":"gear"}).table
    table_body = table.find('tbody')
    weapons = {}
    Rrows = set(table_body.find_all('tr'))
    Crows = set(table_body.find_all('tr','delimiter'))
    result = list(Rrows - Crows)
    for r in reversed(result):
        nm = r.find("td",{"class":"gearTitle"}).a.div.text
        ef = r.find("td",{"class":"gearEffect"}).div.text
        if r.find("span",{"class":"attrBlock silver"}):
            continue
        try:
            cp = r.find_all("span","attrBlock")[1].text
        except IndexError:
            cp = "Cannot be equipped"
        nm = "{} CP: {}".format(nm,cp)
        weapons[nm] = ef.encode("ascii", "replace").decode().replace("?"," ")

    return {"Name":name,
            "Crystal":crystal,
            "Weapon":weapon,
            "Picture":pictureurl,
            "Stats":stats,
            "Commands":commands,
            #"Artifacts":artifacts,
            "Passives":passives,
            "Weapons":weapons}



def update_db():
    retrieveNames()
    CHARACTERS = json.loads(open('dependencies/{}/charnames.json'.format(LOCALE),'r').read())
	for i in CHARACTERS.values():
	    with open('dependencies/{}/{}.json'.format(LOCALE,i),'w') as u:
	        json.dump(getCharacter(i),u)



def full_update():
    LOCALE = "GL"
    update_db()
    LOCALE = "JP"
    update_db()



