import json
import pandas as pd
import plotly.express as px

def graph(file, projectid, data: json):
    inputdata = []
    ano = []

    for U in data['entries']:
        username = U['displayName']
        points_all = U['totalPoints']
        points_valid = U['validatedPoints']
        points_invalid = U['invalidatedPoints']
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
    df = df.sort_values(by=["good", "pending"])
    fig = px.bar(df, title=f"Leaderboard for Project {data['projectName']} ({projectid})", orientation='h', y='User',
                 x=['good', 'pending', 'bad'], labels=dict(index="Users", value="Tasks", variable="Task stats"))

    fig._data[0]["marker"]['color'] = "rgba(43, 158, 0, 1)"
    fig._data[1]["marker"]['color'] = "rgba(0, 149, 166, 1)"
    fig._data[2]["marker"]['color'] = "rgba(126, 2, 184, 1)"

    fig.update_layout(annotations=ano, plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', font_size=24)
    fig.write_image(file, width=1920, height=1080)

def pie(file, projectid, data: json):
    inputdata = []
    ano = []

    for U in data['entries']:
        username = U['displayName']
        points_all = U['totalPoints']
        points_valid = U['validatedPoints']
        points_invalid = U['invalidatedPoints']
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
    df = df.sort_values(by=["good", "pending"])
    fig = px.pie(df, title=f"Leaderboard for Project {data['projectName']} ({projectid})",  values='good', labels=dict(index="Users", value="Tasks", variable="Task stats"))

    #fig._data[0]["marker"]['color'] = "rgba(43, 158, 0, 1)"
    #fig._data[1]["marker"]['color'] = "rgba(0, 149, 166, 1)"
    #fig._data[2]["marker"]['color'] = "rgba(126, 2, 184, 1)"


    fig.update_layout(annotations=ano, plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)', font_size=24)
    fig.write_image("./test.png", width=1920, height=1080)