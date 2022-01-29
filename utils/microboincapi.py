import json

import requests
from config.config import microboincapikey, microboincapi_endpoint

header = {'Authorization': microboincapikey, 'user-agent': 'realN00bBot/0.0.1'}

def register(nickname: str, discordid: int):
    r = requests.post(url=f"{microboincapi_endpoint}/accounts", headers=header,
                      json={
                              "DisplayName": f"{nickname}",
                              "DiscordID": discordid
                          })

    if r.status_code == 200:
        return True, r.json()['key']
    elif r.status_code == 409:
        return False, "An API-Key already exists!"
    else:
        return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)



def getleaderboardbyid(appid: int):
    r = requests.get(url=f"{microboincapi_endpoint}/leaderboards/byproject/{appid}", headers=header)
    if r.status_code == 200:
        return True, r.json()
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def gethistleaderboardbyid(appid: int):
    r = requests.get(url=f"{microboincapi_endpoint}/leaderboards/byproject/{appid}/historical", headers=header)

    if r.status_code == 200:
        return True, r.json()
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)

def getleaderboardbyidforuser(appid: int, discordid: int):
    r = requests.get(url=f"{microboincapi_endpoint}/leaderboards/byproject/{appid}/{discordid} ", headers=header)

    if r.status_code == 200:
        return True, r.json()
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)

def getresultsbyappid(appid: int):
    r = requests.get(url=f"{microboincapi_endpoint}/results/byprojectid/{appid}", headers=header)

    if r.status_code == 200:
        return True, str(r.content)[2:-1].replace("\\n", "\n")
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)