import json

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
#        "showlegend": True,
#        "barmode": "stack",
#        "bargap": 0.618,
#        "annotations": []


    for U in data['Leaderboard']:
        pending = U['Points'] - U['ValidatedPoints'] - U['InvalidatedPoints']
        ano.append({
            "y": U['User']['Username'],
            "x": U['Points'],
            "text": U['Points'] - U['InvalidatedPoints'],
            "xanchor": "left",
            "yanchor": "middle",
            "showarrow": False
        })

        inputdata.append([U['User']['Username'], U['ValidatedPoints'], pending, U['InvalidatedPoints']])

    df = pd.DataFrame(inputdata, columns=["User", "good", "pending", "bad"])
    fig = px.bar(df, title=f"Leaderboard for Project {projectid}", orientation='h', y='User',
                 x=['good', 'pending', 'bad'], labels=dict(index="Users", value="Tasks"))  # , text="value")

    fig._data[0]["marker"]['color'] = "rgba(43, 158, 0, 1)"
    fig._data[1]["marker"]['color'] = "rgba(0, 149, 166, 1)"
    fig._data[2]["marker"]['color'] = "rgba(126, 2, 184, 1)"

    # fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    # fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(annotations=ano, barmode="stack")
    fig.update_layout(plot_bgcolor='rgba(33, 40, 51, 1)', paper_bgcolor='rgba(33, 40, 51, 1)',
                      font_color='rgba(196, 222, 255, 1)')
    fig.show()
    fig.write_image(file)
