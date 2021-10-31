import json
from datetime import datetime

import pandas as pd
import plotly.express as px

testdata = [
    ["User1", 10, 6, 1],
    ["User2", 8, 4, 1],
    ["User3", 5, 2, 0],
    ["User4", 2, 2, 3]
]


def graph(file, projectid, data: json):
    inputdata = []
    ano = []

    for U in data['Leaderboard']:
        username = U['User']['Username']
        points_all = U['Points']
        points_valid = U['ValidatedPoints']
        points_invalid = U['InvalidatedPoints']
        pending = points_all - points_valid - points_invalid
        ano.append({
            "y": username,
            "x": points_all,
            "text": str(points_valid) + " | " + str(pending) + " | " + str(points_invalid),
            "xanchor": "left",
            "yanchor": "middle",
            "showarrow": False
        })

        inputdata.append([username, points_valid, pending, points_invalid])

    df = pd.DataFrame(inputdata, columns=["User", "good", "pending", "bad"])
    fig = px.bar(df, title=f"Leaderboard for Project {projectid}", orientation='h', y='User',
                 x=['good', 'pending', 'bad'], labels=dict(index="Users", value="Tasks", variable="Task stats"))

    fig._data[0]["marker"]['color'] = "rgba(43, 158, 0, 1)"
    fig._data[1]["marker"]['color'] = "rgba(0, 149, 166, 1)"
    fig._data[2]["marker"]['color'] = "rgba(126, 2, 184, 1)"

    fig.update_layout(annotations=ano, plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', font_size=24)
    fig.write_image(file, width=1920, height=1080)


def multipower(file, projectid, data):
    inputdata = {}
    last = {}
    for l in data.split("\n"):
        uid, ps, vps, ivps, ts = l.split(" ")
        # ps = int(ps)
        vps = int(vps)
        # ivps = int(ivps)

        if vps > last.setdefault(uid, 0):
            inputdata.setdefault(int(uid), {})[
                datetime.fromtimestamp(int(ts)).replace(microsecond=0, second=0).isoformat()] = vps
            last[uid] = vps

    df = pd.DataFrame.from_dict(inputdata)
    df.sort_index(axis=0, inplace=True)
    df.sort_index(axis=1, inplace=True)

    fig = px.line(df, title=f'Valid points over time for project: {projectid}',
                  labels={"index": "Time", "value": "Valid tasks", "variable": "Users"})
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)

def singlepower(file, userid, username, data):
    l1, l2, l3 = 0, 0, 0
    inputdata = {}
    for l in data.split("\n"):
        uid, ps, vps, ivps, ts = l.split(" ")
        ps = int(ps)
        vps = int(vps)
        ivps = int(ivps)

        if int(uid) == int(userid):
            if ps >= l1 and vps >= l2 and ivps >= l3:
                l1, l2, l3 = ps, vps, ivps
                iso = datetime.fromtimestamp(int(ts)).replace(microsecond=0, second=0).isoformat()
                inputdata.setdefault("points", {})[iso] = ps
                inputdata.setdefault("validpoints", {})[iso] = vps
                inputdata.setdefault("invalidpoints", {})[iso] = ivps

    df = pd.DataFrame.from_dict(inputdata)
    df.sort_index(axis=0, inplace=True)

    fig = px.line(df, title=f"Power over time from: {username}",
                  labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    if 0 < len(fig._data): fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    if 1 < len(fig._data): fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    if 2 < len(fig._data): fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)

def totalpower(file, data):
    last = {}
    inputdata = {}
    sps, svps, sivps = 0, 0, 0


    for l in data.split("\n"):
        uid, ps, vps, ivps, ts = l.split(" ")
        ps = int(ps)
        vps = int(vps)
        ivps = int(ivps)
        ts = int(ts)

        if ps > last.setdefault(uid, {}).setdefault("ps", 0):
            sps += 1
        elif vps > last.setdefault(uid, {}).setdefault("vps", 0):
            svps += 1
        elif ivps > last.setdefault(uid, {}).setdefault("ivps", 0):
            sivps += 1

        iso = datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()

        inputdata.setdefault("points", {})[iso] = sps
        inputdata.setdefault("validpoints", {})[iso] = svps
        inputdata.setdefault("invalidpoints", {})[iso] = sivps

        last[uid]["ps"] = ps
        last[uid]["vps"] = vps
        last[uid]["ivps"] = ivps

    df = pd.DataFrame.from_dict(inputdata)
    df.sort_index(axis=0, inplace=True)

    fig = px.line(df, title='Total power over time', labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')
    fig.write_image(file, width=1920, height=1080)



def totalhourlypower(file, data):
    last = {}
    inputdata = {}

    for l in data.split("\n"):
        uid, ps, vps, ivps, ts = l.split(" ")
        ps = int(ps)
        vps = int(vps)
        ivps = int(ivps)
        ts = int(ts)

        iso = datetime.fromtimestamp(ts).replace(microsecond=0, second=0, minute=0).isoformat()
        if ps > last.setdefault(uid, {}).setdefault("ps", 0):
            inputdata.setdefault("points", {}).setdefault(iso, []).append("1")
        elif vps > last.setdefault(uid, {}).setdefault("vps", 0):
            inputdata.setdefault("validpoints", {}).setdefault(iso, []).append("1")
        elif ivps > last.setdefault(uid, {}).setdefault("ivps", 0):
            inputdata.setdefault("invalidpoints", {}).setdefault(iso, []).append("1")

        last[uid]["ps"] = ps
        last[uid]["vps"] = vps
        last[uid]["ivps"] = ivps

    nl = {}
    for pt in inputdata.keys():
        for ht in inputdata[pt].keys():
            nl.setdefault(pt, {})[ht] = len(inputdata[pt][ht])

    df = pd.DataFrame.from_dict(nl)

    fig = px.line(df, title="Hourly stats over time", labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)

def singlehourlypower(file, userid, username, data):
    last = {}
    inputdata = {}

    for l in data.split("\n"):
        uid, ps, vps, ivps, ts = l.split(" ")
        ps = int(ps)
        vps = int(vps)
        ivps = int(ivps)
        ts = int(ts)

        if int(uid) == int(userid):
            if ps > last.setdefault("ps", 0):
                iso = datetime.fromtimestamp(ts).replace(microsecond=0, second=0, minute=0).isoformat()
                inputdata.setdefault("ps", {}).setdefault(iso, []).append("1")
            if vps > last.setdefault("vps", 0):
                iso = datetime.fromtimestamp(ts).replace(microsecond=0, second=0, minute=0).isoformat()
                inputdata.setdefault("vps", {}).setdefault(iso, []).append("1")
            if ivps > last.setdefault("ivps", 0):
                iso = datetime.fromtimestamp(ts).replace(microsecond=0, second=0, minute=0).isoformat()
                inputdata.setdefault("ivps", {}).setdefault(iso, []).append("1")

            last["ps"] = ps
            last["vps"] = vps
            last["ivps"] = ivps

    nl = {}
    for pt in inputdata.keys():
        for ht in inputdata[pt].keys():
            nl.setdefault(pt, {})[ht] = len(inputdata[pt][ht])

    df = pd.DataFrame.from_dict(nl)

    fig = px.line(df, title=f"Hourly stats over time for: {username}", labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    if 0 < len(fig._data): fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    if 1 < len(fig._data): fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    if 2 < len(fig._data): fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)
