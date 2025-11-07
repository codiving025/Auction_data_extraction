from bs4 import BeautifulSoup
import requests
link = 'https://www.cricbuzz.com/cricket-team/india/2/players'
link2= 'https://www.cricbuzz.com'
list1 = []
palyerinfo_dict = {}
def extractions(link):
    source = requests.get(link).text
    soup = BeautifulSoup(source,'html.parser')
    return soup

player_html =  extractions
content = player_html(link).find_all('div',class_= 'flex flex-col gap-px tb:grid tb:grid-cols-2')
# print(content)
# make link  for evryplayer profile
for item in content:
    list1.append(link2+f'{item.a['href']}')    

raw_content = player_html(list1[0])
for each_player in raw_content.find_all('div',class_='w-full col-span-1'):
        print(f'name:{each_player.span.text} , img:{each_player.div.img['srcset']}')
# for player in list1:
#     raw_content = player_html(player)
#     for each_player in raw_content.find_all('div',class_='w-full col-span-1'):
#         print(each_player)
#     print(img)
    # print(f'img:{} ,category:{} ,team_country:{} ,batting_style:{} , bolling_style:{} ,teams_played: {}')
