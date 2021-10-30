import json

import requests
import mysql.connector
from config.config import mattapikey, miniboincapi_host, mysql_host, mysql_user, mysql_password

header = {'Authorization': mattapikey, 'user-agent': 'microboinc Bot/0.0.1'}


def register(nickname: str, discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/accounts/register", headers=header,
                      json={
                          "User": {
                              "Username": f"{nickname}",
                              "DiscordID": discordid
                          }})

    if r.status_code == 200:
        return True, r.json()['APIKey']
    elif r.status_code == 400:
        return False, "Pls use only the following characters: a-z A-Z _ -"
    elif r.status_code == 409:
        return False, "An API-Key already exists!"
    else:
        return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def regen(discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/accounts/regen/bydiscordid", headers=header,
                      json={
                          "DiscordID": discordid
                      })

    if r.status_code == 200:
        return True, r.json()['APIKey']
    else:
        return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)

def getuserinfobyid(discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/accounts/query/basic/bydiscordid", headers=header,
                      json={
                          "DiscordID": discordid
                      })

    if r.status_code == 200:
        return True, r.json()
    elif r.status_code == 400:
        return False, "You don't have a API-Key yet."
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)

def getapilevelbyid(discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/accounts/query/basic/bydiscordid", headers=header,
                      json={
                          "DiscordID": discordid
                      })

    if r.status_code == 200:
        return True, r.json()['User']['AdminLevel']
    elif r.status_code == 400:
        return False, "You don't have a API-Key yet."
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def isapilevelbyid(discordid: int, level: int):
    suc, res = getapilevelbyid(discordid)
    if suc:
        if res >= level:
            return True
    return False


def deletebyid(discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/accounts/vaporise/user/bydiscordid", headers=header,
                      json={
                          "DiscordID": discordid
                      })

    if r.status_code == 200:
        return True, "User deleted."
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def getresultsbyappid(appid: int):
    r = requests.post(url=f"{miniboincapi_host}/tasks/query/outputs/byappid", headers=header,
                      json={
                          "MetaID": appid
                      })

    if r.status_code == 200:
        return True, str(r.content)[2:-1].replace("\\n", "\n")
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def getprogressbyappid(appid: int):
    r = requests.post(url=f"{miniboincapi_host}/tasks/query/progress/bymetaid", headers=header,
                      json={
                          "ID": appid
                      })

    if r.status_code == 200:
        return True, json.loads(str(r.content)[2:-1].replace("\\n", "\n"))
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def getleaderboardbyid(appid: int):
    r = requests.post(url=f"{miniboincapi_host}/leaderboard/current", headers=header,
                      json={
                          "MetadataID": appid
                      })

    if r.status_code == 200:
        return True, json.loads(str(r.content)[2:-1].replace("\\n", "\n"))
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def gethistleaderboardbyid(appid: int):
    r = requests.post(url=f"{miniboincapi_host}/leaderboard/historical/byprojectid", headers=header,
                      json={
                          "MetadataID": appid
                      })

    if r.status_code == 200:
        return True, str(r.content)[2:-1].replace("\\n", "\n")
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def getleaderdb(pid: int, validated: bool = True):
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password
    )

    mycursor = mydb.cursor()
    mycursor.execute("USE pseudobanic;")
    if validated:
        mycursor.execute(
            f"SELECT COUNT(*) AS count, username FROM assignments JOIN tasks ON assignments.task_id = tasks.task_id JOIN users ON assignments.userid = users.userID WHERE task_metaid = {pid} and state = 1 and task_status = 2 GROUP BY users.userid ORDER BY count DESC;")
    else:
        mycursor.execute(
            f"SELECT COUNT(*) AS count, username FROM assignments JOIN tasks ON assignments.task_id = tasks.task_id JOIN users ON assignments.userid = users.userID WHERE task_metaid = {pid} and state = 1 and task_status = 1 GROUP BY users.userid ORDER BY count DESC;")
    myresult = mycursor.fetchall()
    return myresult
