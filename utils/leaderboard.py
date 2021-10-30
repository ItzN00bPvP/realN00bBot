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
                datetime.fromtimestamp(int(ts)).replace(microsecond=0, second=0).isoformat()] = vps  # ,minute=0
            last[uid] = vps

    df = pd.DataFrame.from_dict(inputdata)
    df.sort_index(axis=0, inplace=True)

    fig = px.line(df, title=f'Valid points over time for project: {projectid}', labels={"index": "Time", "value": "Valid tasks", "variable": "Users"})
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', legend_bgcolor='rgba(76, 91, 115, 1)', font_size=24)
    fig.update_traces(connectgaps=True)
    fig.update_xaxes(type='date')

    fig.write_image(file, width=1920, height=1080)