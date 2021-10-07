import pandas as pd
import plotly.express as px


testdata = [
    ["User1", 10, 6, 1],
    ["User2", 8,4,1],
    ["User3", 5,2,0],
    ["User4", 2,2,3]
]

def graph(file, data):

    inputdata =[]

    for U in data['Leaderboard']:
        pending = U['Points'] - U['ValidatedPoints'] - U['InvalidatedPoints']
        inputdata.append([U['User']['Username'], U['ValidatedPoints'], pending, U['InvalidatedPoints']])


    df = pd.DataFrame(inputdata, columns=["User", "good", "pending", "bad"])
    fig = px.bar(df, x=['good', 'pending', 'bad'], y='User', orientation='h')

    fig._data[0]["marker"]['color'] = "rgba(43, 158, 0, 1)"
    fig._data[1]["marker"]['color'] = "rgba(0, 149, 166, 1)"
    fig._data[2]["marker"]['color'] = "rgba(126, 2, 184, 1)"

    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)')

    fig.write_image(file)

graph(file="fig.png", data=testdata)
