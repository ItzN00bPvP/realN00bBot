import pandas as pd
import plotly.express as px
from datetime import datetime
import time

def multipower(file, projectid, data):
    inputdata = {}

    for U in data['entries']:
        username = U['displayName']
        #points_all = U['totalPoints']
        points_valid = U['validStamps']
        #points_invalid = U['invalidatedPoints']
        #points_pending = points_all - points_valid - points_invalid

        #points.setdefault(username, {})["points_all"] += 1
        #points.setdefault(username, {})["points_valid"] += 1
        #points.setdefault(username, {})["points_invalid"] += 1
        #points.setdefault(username, {})["points_pending"] += 1

        p = 1
        for ts in points_valid:
            inputdata.setdefault(username, {})[datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()] = p
            p += 1

    df = pd.DataFrame.from_dict(inputdata)
    df.sort_index(axis=0, inplace=True)
    df.sort_index(axis=1, inplace=True)

    fig = px.line(df, title=f'Valid points over time for Project {data["projectName"]} ({projectid})',
                  labels={"index": "Time", "value": "Valid tasks", "variable": "Users"})
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)

def singlepower(file, projectid, userid, username, data):
    l1, l2, l3 = 0, 0, 0
    inputdata = {}

    for U in data['entries']:
        username = U['displayName']
        points_all = U['totalPoints']
        points_valid = U['validStamps']
        points_invalid = U['invalidatedPoints']
        points_pending = points_all - points_valid - points_invalid

        #points.setdefault(username, {})["points_all"] += 1
        #points.setdefault(username, {})["points_valid"] += 1
        #points.setdefault(username, {})["points_invalid"] += 1
        #points.setdefault(username, {})["points_pending"] += 1

        p = 1
        for ts in points_valid:
            inputdata.setdefault(username, {})[datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()] = p
            p += 1
        p = 1
        for ts in points_pending:
            inputdata.setdefault(username, {})[datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()] = p
            p += 1


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

    fig = px.line(df, title=f"Points over time from: {username} Project: {projectid}",
                  labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    if 0 < len(fig._data): fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    if 1 < len(fig._data): fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    if 2 < len(fig._data): fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)

def totalpower(file, projectid, data):
    start = time.process_time()
    #elapsed_time = time.process_time() - start
    #print(f"looping sorting time: {elapsed_time}")

    inputdata = {}

    total_submittedstamps = []
    total_validstamps = []
    total_invalidstamps = []


    for U in data['entries']:
        total_submittedstamps += U['submittedStamps']
        total_validstamps += U['validStamps']
        total_invalidstamps += U['invalidStamps']

    total_submittedstamps.sort()
    total_validstamps.sort()
    total_invalidstamps.sort()


    p = 1
    for ts in total_submittedstamps:
        inputdata.setdefault("points", {})[datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()] = p
        p += 1
    p = 1
    for ts in total_validstamps:
        inputdata.setdefault("validpoints", {})[datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()] = p
        p += 1
    p = 1
    for ts in total_invalidstamps:
        inputdata.setdefault("invalidpoints", {})[datetime.fromtimestamp(ts).replace(microsecond=0, second=0).isoformat()] = p
        p += 1

    elapsed_time = time.process_time() - start
    print(f"looping sorting time: {elapsed_time}")

    df = pd.DataFrame.from_dict(inputdata)
    #df.sort_index(axis=0, inplace=True)


    fig = px.line(df, title=f"Total power over time Project: {projectid}",
                  labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    if 0 < len(fig._data): fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    if 1 < len(fig._data): fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    if 2 < len(fig._data): fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')
    fig.write_image(file, width=1920, height=1080)



def totalhourlypower(file, projectid, data):
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

    fig = px.line(df, title=f"Hourly stats over time Project: {projectid}",
                  labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    if 0 < len(fig._data): fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    if 1 < len(fig._data): fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    if 2 < len(fig._data): fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)

def singlehourlypower(file, projectid, userid, username, data):
    last = {}
    inputdata = {}

    for l in data.split("\n"):
        uid, ps, vps, ivps, ts = l.split(" ")
        ps = int(ps)
        vps = int(vps)
        ivps = int(ivps)
        ts = int(ts)

        if int(uid) == int(userid):
            iso = datetime.fromtimestamp(ts).replace(microsecond=0, second=0, minute=0).isoformat()
            if ps > last.setdefault("ps", 0):
                inputdata.setdefault("points", {}).setdefault(iso, []).append("1")
            if vps > last.setdefault("vps", 0):
                inputdata.setdefault("validpoints", {}).setdefault(iso, []).append("1")
            if ivps > last.setdefault("ivps", 0):
                inputdata.setdefault("invalidpoints", {}).setdefault(iso, []).append("1")

            last["ps"] = ps
            last["vps"] = vps
            last["ivps"] = ivps

    nl = {}
    for pt in inputdata.keys():
        for ht in inputdata[pt].keys():
            nl.setdefault(pt, {})[ht] = len(inputdata[pt][ht])

    df = pd.DataFrame.from_dict(nl)

    fig = px.line(df, title=f"Hourly stats over time from: {username} Project: {projectid}",
                  labels={"index": "Time", "value": "Tasks", "variable": "Info:"})
    if 0 < len(fig._data): fig._data[0]["line"]['color'] = "rgba(0, 149, 166, 1)"
    if 1 < len(fig._data): fig._data[1]["line"]['color'] = "rgba(43, 158, 0, 1)"
    if 2 < len(fig._data): fig._data[2]["line"]['color'] = "rgba(126, 2, 184, 1)"
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)
