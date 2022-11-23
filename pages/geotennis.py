# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

# get all ATP Ranking Dates
with open('m/rank/dates.txt') as f:
    all_dates = [date[:-1] for date in f]

# load txt files
def load_txt(file):
    with open(file, 'r', encoding='utf-8-sig') as f:
        attributes = f.readline()[:-1].split(',')
        df = pd.DataFrame([line[:-1].split(',') for line in f], columns = attributes)
    f.close()
    return df

# define function to visualize ATP Top 100 geographics
def atp100geo():
    df = load_txt('m/rank/atp100geo20002022.txt')
    df = df.replace('', np.NaN)
    for attr in ['Rank', 'Points', 'Lat', 'Lon']:
        tmp = []
        for item in df[attr]:
            tmp.append(pd.to_numeric(item))
        df[attr] = tmp
    token = 'pk.eyJ1IjoiamVycnljZyIsImEiOiJjbGFydTRnd2wxb2VrM3dtcWQwemEzcHZyIn0.omMUwd3eoo_OOLhX9uzjwg'

    fig = px.scatter_mapbox(df, lat="Lat", lon="Lon", hover_name="Player", hover_data=["Rank", "Points", "Birthplace"], color="Points", size = "Points",
                            color_discrete_sequence=["fuchsia"], zoom=1, mapbox_style="open-street-map", height=500,
   #                         animation_frame="Date", animation_group="Player", 
                            template="plotly_dark")

    fig.update_layout(mapbox_style="dark", mapbox_accesstoken=token)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_mapboxes(bounds={"west": min(df['Lon']), "east": max(df['Lon']), "south": min(df['Lat']), "north": max(df['Lat'])})
    fig.update_mapboxes(center={'lat':sum(df['Lat'])/len(df), 'lon':sum(df['Lon']/len(df))})
    return fig

# create app
dash.register_page(__name__, name = 'GeoTennis')

layout = html.Div(children=[
    # section display a given ATP Ranking Date's Top 100 Players geographic distribution
    html.Div(children=[
        html.H2('ATP Top100 Players Geographical Distribution', style = {'padding-left':'10px'}),
        dcc.Loading(dcc.Graph(id='atp100geo', figure = atp100geo()), type='cube'),  
    ]),
]
)


