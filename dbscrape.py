from selenium import webdriver
from bs4 import BeautifulSoup
import json

browser=webdriver.Firefox()
def bs_parse(url):
    browser.get(url)
    html = browser.page_source
    return BeautifulSoup(html, 'lxml')

# Links
root = "https://dissidiadb.com"
charpage = "/characters"


# Retrieve Page Name
charpage = bs_parse(root+charpage)
lst= charpage.body.div.main.div.ul    

charnames = [l.find("span",{"class":"name"}).string for l in lst] # use this for their name
charurl = [l.find("a",{"class":"imageLink"})['href'][1:] for l in lst]
chars = dict(zip(charnames,charurl))


# Dumps Character Info
def getCharacter(charName):
    soup = bs_parse(root+"/"+charName)
    
    # Retrieve Crystal Type and Weapon type
    crystal = soup.find("span",{"class":"icon crystal"})['title']
    weapon = soup.find("p",{"class":"weapon-type"}).find("span",{"class":"icon"})['title']


    # Retrieve Name
    name = soup.find("h2",{"class":"header"}).string

    # Retrieve Picture URL
    picture = soup.find("div",{"class":"bgImage"})['style']
    start_pt = picture.find("\"")
    end_pt = picture.find("\"", start_pt + 1)
    picture = picture[start_pt + 1: end_pt]
    pictureurl = root+picture

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
        commands[cols] = nmn.text # Get rid of empty values


    # Retrieve Passive Abilities
    table = soup.find("div",{"class":"passives"}).table
    table_body = table.find('tbody')
    passives = {}
    rows = table_body.find_all('tr')
    for row in rows:
        comb = row.find_all('td')
        n = comb[0].find_all('div')[0].text
        e = comb[1].find_all('div')[0].text
        passives[n] = e # Get rid of empty values


    # Retrieve Artifact passives list
    table = soup.find("div",{"class":"artifacts"}).table
    table_body = table.find('tbody')
    artifacts = {}
    rows = table_body.find_all('tr')
    cutrows = []
    for i in range(0,len(rows),2):
        cutrows.append([rows[i],rows[i+1]])
        
    for row in cutrows:
        
        n = row[0].find("td",{"class":"passive"}).find_all("div")[0].text
        effect = row[1].find('td',{"class":"effect max"}).text
        artifacts[n] = effect # Get rid of empty values
    
    
    return {"Name":name,
            "Crystal":crystal,
            "Weapon":weapon,
            "Picture":pictureurl,
            "Stats":stats,
            "Commands":commands,
            "Artifacts":artifacts,
            "Passives":passives}

for i in chars.values():
    #print(i)
    with open(i+'.json','w') as u:
        json.dump(getCharacter(i),u)

