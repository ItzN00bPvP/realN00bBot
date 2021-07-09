import requests
from config.config import mattapikey, miniboincapi_host

header = {'Authorization': mattapikey, 'user-agent': 'microboinc Bot/0.0.1'}


def register(nickname: str, discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/register", headers=header,
                          json={
                              "User": {
                                  "Username": f"{nickname}",
                                  "DiscordID": discordid
                              }})

    if r.status_code != 200:
        if r.status_code == 400:
            return False, "Pls use only the following characters: a-z A-Z _ -"
        elif r.status_code == 409:
            return False, "An API-Key already exists!"
        else:
            return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)

    return True, r.json()['APIKey']



