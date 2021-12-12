from django.db.models import base
from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
from .models import Player
from django.forms.models import model_to_dict

# Create your views here.
base_url=''
def home(request):
    global base_url
    if request.method=="POST":
        web_url=request.POST.get("weburl")
        base_url=web_url.split('.com',1)[0]+'.com'
        print(base_url)
        req=requests.get(web_url)
        html=req.content
        
        soup=BeautifulSoup(html, 'html.parser')
        # print(soup.prettify())

        for h in soup.find_all('li', class_='nav-item'):
            try:
                if h.find('a', class_='nav-link').get_text().lower()=="squads":
                    atag=h.find('a', class_='nav-link')
                    try:
                        link=atag['rel']
                        getSquad(base_url+atag['href'])
                    except:
                        getSquad(atag['href'])
                        
                    break
            except:
                continue

    if request.method=="GET":
        squadname=request.GET.get("squadname").lower()
        mod=Player.objects.filter(player_team=squadname)
        content=[]
        for p in mod:
            dic={}
            dic["name"]=p.player_name
            dic["skill"]=p.player_skill
            dic["team"]=p.player_team
            content.append(dic)
        print(content)
        return render(request, 'home.html', {"data":content})
    return render(request, 'home.html', {})


def getSquad(squadLink):
    global base_url
    print(squadLink)
    req=requests.get(squadLink)
    html=req.content

    soup=BeautifulSoup(html, 'html.parser')
    # print(soup.prettify())

    table=soup.find('h2',class_='squads-squad-title').find_next_sibling('div')
    atags=[]
    # print(table.find_all('div', class_='squad-row'))
    for sib in table.findChildren('div',recursive=False):
        atags.append(sib.findChildren('div')[0].find('a'))
    for a in atags:
        try:
            link=a['rel']
            getSquadMembers(base_url+a['href'],a.get_text())
        except:
            getSquadMembers(a['href'],a.get_text())


def getSquadMembers(teamLink, teamName):
    req=requests.get(teamLink)
    html=req.content

    soup=BeautifulSoup(html, 'html.parser')
    playersContent=soup.find_all('div', class_='squad-player')
    for player in playersContent:
        play=Player()
        playerName=player.findChildren('div')[2].findChildren('div')[1].find('a').get_text()
        playerSkill=player.findChildren('div')[2].findChildren('div')[2].get_text()
        
        print(teamName)

        if Player.objects.filter(player_name=playerName, player_skill=playerSkill, player_team=teamName):
            print("ok")
        else:
            play.player_name=playerName.lower()
            play.player_skill=playerSkill.lower()
            play.player_team=teamName.lower()
            play.save()

        # print(player.findChildren('div')[2].findChildren('div')[1].find('a').get_text())
        # print(player.findChildren('div')[2].findChildren('div')[2].get_text())
    # print(playerName)
    # print(playerSkill)
