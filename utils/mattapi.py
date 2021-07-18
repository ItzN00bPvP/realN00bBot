import requests
import mysql.connector
from config.config import mattapikey, miniboincapi_host, mysql_host, mysql_user, mysql_password

header = {'Authorization': mattapikey, 'user-agent': 'microboinc Bot/0.0.1'}


def register(nickname: str, discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/register", headers=header,
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


def getapilevelbyid(discordid: int):
    r = requests.post(url=f"{miniboincapi_host}/query/basic/bydiscordid", headers=header,
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
    r = requests.post(url=f"{miniboincapi_host}/vaporise/user/bydiscordid", headers=header,
                      json={
                          "DiscordID": discordid
                      })

    if r.status_code == 200:
        return True, "User deleted."
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def getresultsbyappid(appid: int):
    r = requests.post(url=f"{miniboincapi_host}/stream/outputs/byappid", headers=header,
                      json={
                          "MetaID": appid
                      })

    if r.status_code == 200:
        return True, str(r.content)[2:-1].replace("\\n", "\n")
    elif r.status_code == 404:
        return False, "App not found!"
    return False, "<@374245848659263488> something went wrong code: " + str(r.status_code)


def getleaderdb(pid: int):
    mydb = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password
    )

    mycursor = mydb.cursor()
    mycursor.execute("USE pseudobanic;")
    mycursor.execute(
        f"SELECT COUNT(*) AS count, username FROM assignments JOIN tasks ON assignments.task_id = tasks.task_id JOIN users ON assignments.userid = users.userID WHERE task_metaid = {pid} and state = 1 GROUP BY users.userid ORDER BY count DESC;")
    myresult = mycursor.fetchall()
    return myresult
