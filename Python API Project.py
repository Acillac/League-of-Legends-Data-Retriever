import requests
import pandas as pd
import time
api_key = "RGAPI-bd6e9133-e78b-430e-bbdf-0333b94e90a5"
summoner_name = "Acillac"
mass_region = "ASIA"
num_games = 20
region = "kr"
queue_id = 450

# USER INTERFACE
summoner_name = input("Hello, please input your summoner name: ")
region = input("Thanks " + summoner_name + ". Please enter your region[na1, euw1, eun1, jp1, kr, br1, la1, la2, oc1, ru, tr1]: ")
if (region == "na1" or region == "br1" or region == "la1" or region == "la2") :
    mass_region = "AMERICAS"
if (region == "euw1" or region == "eun1" or region == "ru" or region == "tr1" or region == "oc1") :
    mass_region = "EUROPE"
if (region == "jp1" or region == "kr") :
    mass_region = "ASIA"
gamemode_test = input("Which gamemode history would you like to view? 0[Draft], 1[Ranked], 2[Aram]: ")
if (gamemode_test == "0") :
    queue_id = 400
if (gamemode_test == "1") :
    queue_id = 420
if (gamemode_test == "2") :
    queue_id = 450
num_games = input("How many match history games would you like to view: ")
num_games

# FUNCTIONS
def get_puuid(summoner_name, region, api_key):
    api_url = (
        "https://" +
        region +
        ".api.riotgames.com/lol/summoner/v4/summoners/by-name/" +
        summoner_name +
        "?api_key=" +
        api_key
    )
    response = requests.get(api_url)
    player_info = response.json()
    puuid = player_info["puuid"]
    return puuid

puuid = get_puuid(summoner_name, region, api_key)

def get_match_ids(puuid, mass_region, num_games, queue_id, api_key):
    api_url = (
        "https://" +
        mass_region +
        ".api.riotgames.com/lol/match/v5/matches/by-puuid/" +
        puuid + 
        "/ids?start=0&count=" +
        str(num_games) + 
        "&queue=" +
        str(queue_id) +
        "&api_key=" + 
        api_key
    )
    response = requests.get(api_url)
    match_ids = response.json()
    return match_ids

match_ids = get_match_ids(puuid, mass_region, num_games, queue_id, api_key)

def get_match_data(match_id, mass_region, api_key):
    api_url = (
        "https://" + 
        mass_region + 
        ".api.riotgames.com/lol/match/v5/matches/" +
        match_id + 
        "?api_key=" + 
        api_key
    )
    while True:
        response = requests.get(api_url)
        if response.status_code == 429 :
            time.sleep(10)
            continue
        match_data = response.json()
        return match_data

def find_player_data(match_data, puuid):
    participants = match_data['metadata']['participants']
    player_index = participants.index(puuid)
    player_data = match_data['info']['participants'][player_index]
    return player_data

match_id = match_ids[0]
match_data = get_match_data(match_id, mass_region, api_key)
data = {'champion' : [], 'kills' : [], 'deaths' : [], 'assists' : [], 'win' : []}

def gather_all_data(puuid, match_ids, mass_region, api_key):
    data = {
        'champion': [],
        'kills': [],
        'deaths': [],
        'assists': [],
        'win': []
}
    for match_id in match_ids : 
        match_data = get_match_data(match_id, mass_region, api_key)
        player_data = find_player_data(match_data, puuid)

        champion = player_data['championName']
        k = player_data['kills']
        d = player_data['deaths']
        a = player_data['assists']
        win = player_data['win']
        data['champion'].append(champion)
        data['kills'].append(k)
        data['deaths'].append(d)
        data['assists'].append(a)
        data['win'].append(win)  

    df = pd.DataFrame(data)
    df['win'] = df['win'].astype(int)
    return df
df = gather_all_data(puuid, match_ids, mass_region, api_key)

print(df)
