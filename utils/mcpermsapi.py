import requests
from config.config import apimcathomedev_authtoken

header = {'auth': apimcathomedev_authtoken}


def grantperms(server: str, perms: str, mcname: str, discordid: str):
    req = requests.post(f"https://api.mcathome.dev/mcperms/grant/{server}/{perms}/{discordid}/{mcname}", headers=header)
    if req.status_code == 200:
        return True, req.json()
    return False, f"Something went wrong status: {req.status_code}"


def revokeperms(server: str, user: str):
    req = requests.post(f"https://api.mcathome.dev/mcperms/revoke/{server}/{user}", headers=header)
    if req.status_code == 200:
        return True, req.json()
    return False, f"Something went wrong status: {req.status_code}"


def getglobalperms():
    req = requests.get(f"https://api.mcathome.dev/mcperms/globalperms", headers=header)
    if req.status_code == 200:
        return True, req.json()
    return False, f"Something went wrong status: {req.status_code}"


