import json

import requests
from config.config import microboincapikey, microboincapi_endpoint

header = {'Authorization': microboincapikey, 'user-agent': 'realN00bBot/0.0.1'}


def getleaderboardbyid(appid: int):
    r = requests.get(url=f"{microboincapi_endpoint}/leaderboards/byproject/{appid}", headers=header)
    print(r.status_code)
    if r.status_code == 200:
        return True, json.loads(str(r.content)[2:-1].replace("\\n", "\n"))
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)
