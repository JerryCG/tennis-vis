# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, dash_table
import dash
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import date as dt

# get partial names
all_names = []
with open('mp.txt', 'r') as f:
    cnt = 0
    for line in f:
        all_names.append(line[:-1])
        cnt += 1
        if cnt == 3000:
            break
with open('wp.txt', 'r') as f:
    cnt = 0
    for line in f:
        all_names.append(line[:-1])
        cnt += 1
        if cnt == 3000:
            break


# load txt files
def load_txt(name):
    with open(name[1].lower() + '/matches/txt/' + name[4:] + '.txt', 'r') as f:
        attributes = f.readline()[:-1].split(',')
        df = pd.DataFrame([line[:-1].split(',') for line in f], columns = attributes)
    return (df, name[1])

# define functions to clean df
def clean_df(tuple, date = [None, None]):
    cleaned = tuple[0].replace('', np.NaN)
    cleaned['Date'] = pd.to_datetime(cleaned['Date'])
    # select date if any
    if date != [None, None]:
        if date[0] == None:
            cleaned = cleaned[cleaned['Date'] <= date[1]]
        elif date[1] == None:
            cleaned = cleaned[cleaned['Date'] >= date[0]]
        else:
            cleaned = cleaned[(cleaned['Date'] >= date[0]) & (cleaned['Date'] <= date[1])]

    if tuple[1] == 'M':
        attrs = ['Sets', 'Rk', 'vRk', 'W', 'tRk', 'vtRk', 'DR', 'A%', 'DF%', '1stIn', '1st%', '2nd%', 'TPW', 'RPW', 'vA%', 'v1st%', 'v2nd%', 'TP', 'Aces', 'DFs', 'SP', '1SP', '2SP', 'vA']
    else:
        attrs = ['Sets', 'Rk', 'vRk', 'W', 'tRk', 'vtRk', 'DR', 'A%', 'DF%', '1stIn', '1st%', '2nd%', 'TPW', 'RPW', 'vA%', 'v1st%', 'v2nd%']

    for attr in attrs:
        temp = []
        for item in cleaned[attr]:
            try:
                temp.append(pd.to_numeric(item))
            except:
                try:
                    temp.append(pd.to_numeric(item.strip('%')))
                except:
                    temp.append(np.NaN)
        cleaned[attr] = temp
    return cleaned

# define functions to search for match records
def records(name, date, oppo, surface, match, round, result, streak, layout):
    # name, date, opponent, match name, round, result, show longest win/loss streak, lite/all stats layout
    df = clean_df(load_txt(name), date)
    # select date
    if date != [None, None]:
        if date[0] == None:
            df = df[df['Date'] <= date[1]].reset_index(drop=True)
        elif date[1] == None:
            df = df[df['Date'] >= date[0]].reset_index(drop=True)
        else:
            df = df[(df['Date'] >= date[0]) & (df['Date'] <= date[1])].reset_index(drop=True)
    # select opponent
    if oppo != None:
        df = df[(df['WP'] == oppo[4:]) | (df['LP'] == oppo[4:])].reset_index(drop=True)
    # select surface
    if surface != None:
        df = df[df['Surface'] == surface].reset_index(drop=True)
    # select match
    if match != None:
        if match == 'GS':
            gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']
            df = df[df['Tournament'].isin(gs)].reset_index(drop=True)
        elif match == 'Olympics':
            df = df[df['Tournament'].str.contains('Olympics')].reset_index(drop=True)
        elif match == 'ATP1000':
            atp1000 = ['Indian Wells Masters', 'Miami Masters', 'Monte Carlo Masters', 'Madrid Masters', 'Rome Masters', 'Canada Masters', 'Cincinnati Masters', 'Shanghai Masters', 'Paris Masters', 'Hamburg Masters']
            df = df[df['Tournament'].isin(atp1000)].reset_index(drop=True)
        elif match == 'ATP Finale':
            df = df[df['Tournament'].isin(['Tour Finals', 'Masters Cup'])].reset_index(drop=True)
        else:
            df = df[df['Tournament'] == match].reset_index(drop=True)
    # select round
    if round != None:
        df = df[df['Rd'] == round].reset_index(drop=True)
    # select result
    if result != None:
        if result == 'Win':
            df = df[df['W'] == 1].reset_index(drop=True)
        else:
            df = df[df['W'] == 0].reset_index(drop=True)
    # select streak
    if streak == 'Longest Wins':
        startend = []
        pair = []
        for i in range(len(df)):
            if i == 0:
                if df['W'][i] == 1:
                    pair.append(i)
                if (df['W'][i] == 1) and (df['W'][i + 1] == 0):
                    pair.append(i)
                    startend.append(pair)
                    pair = []
            elif i == len(df) -1:
                if (df['W'][i] == 1) and (df['W'][i - 1] == 0):
                    pair.append(i)
                if df['W'][i] == 1:
                    pair.append(i)
                    startend.append(pair)
                    pair = []
            else:
                if (df['W'][i] == 1) and (df['W'][i - 1] == 0):
                    pair.append(i)
                if (df['W'][i] == 1) and (df['W'][i + 1] == 0):
                    pair.append(i)
                    startend.append(pair)
                    pair = []
        # get the most recent longest streak
        indice = np.argmax([(se[1] - se[0]) for se in startend])
        df = df[[True if (i >= startend[indice][0]) and (i <= startend[indice][1]) else False for i in range(len(df))]].reset_index(drop=True)
    elif streak == 'Longest Losses':
        startend = []
        pair = []
        for i in range(len(df)):
            if i == 0:
                if df['W'][i] == 0:
                    pair.append(i)
                if (df['W'][i] == 0) and (df['W'][i + 1] == 1):
                    pair.append(i)
                    startend.append(pair)
                    pair = []
            elif i == len(df) - 1:
                if (df['W'][i] == 0) and (df['W'][i - 1] == 1):
                    pair.append(i)
                if df['W'][i] == 0:
                    pair.append(i)
                    startend.append(pair)
                    pair = []
            else:
                if (df['W'][i] == 0) and (df['W'][i - 1] == 1):
                    pair.append(i)
                if (df['W'][i] == 0) and (df['W'][i + 1] == 1):
                    pair.append(i)
                    startend.append(pair)
                    pair = []
        # get the most recent longest streak
        indice = np.argmax([(se[1] - se[0]) for se in startend])
        df = df[[True if (i >= startend[indice][0]) and (i <= startend[indice][1]) else False for i in range(len(df))]].reset_index(drop=True)

    # modify date, add Index to facilitate count
    df['Date'] = [str(d)[:10] for d in df['Date']]
    df.insert(loc = 0, column = 'Index', value = [(i + 1) for i in range(len(df))])

    # select layout
    if layout == 'Lite':
        return df[['Index', 'Date', 'Tournament', 'Surface', 'Rd', 'W', 'WP', 'LP', 'Score', 'Time']].to_dict('records')
    else:
        return df.to_dict('records')

# create app
dash.register_page(__name__, name = 'Records Search')

layout = html.Div(children=[
    # section for a record search table
    html.Div(children=[
        html.H2('Select with below criteria to search for match records:'),
        html.Div(children=[
            dcc.DatePickerRange(id="recordsdate",
                start_date_placeholder_text = 'Start Date',
                end_date_placeholder_text = 'End Date',
                className = 'column5',
                clearable = True,
            ),
            dcc.Dropdown(id="recordsname", options = all_names, value = '(M) Novak Djokovic', placeholder = 'Player Name', clearable = False, style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            dcc.Dropdown(id="recordsoppo", options = all_names, placeholder = 'All Opponents', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            dcc.Dropdown(id="recordssurface", options = ['Hard', 'Grass', 'Clay'], placeholder = 'All Surfaces', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            dcc.Dropdown(id="recordsmatch", options = ['GS', 'Wimbledon', 'US Open', 'Australian Open', 'Roland Garros', 'ATP Finale', 'ATP1000', 'Olympics', 'Indian Wells Masters', 'Miami Masters', 'Monte Carlo Masters', 'Madrid Masters', 'Rome Masters', 'Canada Masters', 'Cincinnati Masters', 'Shanghai Masters', 'Paris Masters', 'Hamburg Masters'], placeholder = 'All Tournaments', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            ], className = 'row5'
        ),    
        html.Div(children=[
            dcc.Dropdown(id="recordsround", options = ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F', 'RR'], placeholder = 'All Rounds', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            dcc.Dropdown(id="recordsresult", options = ['Win', 'Lose'], placeholder = 'All Results', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            dcc.Dropdown(id="recordsstreak", options = ['Longest Wins', 'Longest Losses'], placeholder = 'No Streak Selection', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            dcc.Dropdown(id="recordslayout", options = ['Lite', 'All Stats'], clearable = False, value = 'Lite', style = {'background-color': 'rgb(17,17,17)'}, className = 'column5'),
            html.Button("Search Records", id='recordssearch', n_clicks = 0, style = {'padding': '5px', 'margin-top':'10px', 'margin-left': '25px', 'margin-right': 'auto', 'font-size': '20px', 'color': 'gold', 'background-color': 'rgb(17,17,17)', 'border-radius': '12px', 'border-color': 'gold', 'cursor': 'pointer', 'width': '200px'}, className = 'column5'),
            ], className = 'row5',
        ),
        dash_table.DataTable(
            page_size = 100,
            style_table={'height': '350px', 'overflowY': 'auto', 'overflowX': 'auto'},
            id = 'records',
            style_data={
                'whiteSpace': 'normal',
            },
        ),
    ]),
]
)

# records
@dash.callback(
    Output('records', 'data'),
    [Input('recordssearch', 'n_clicks')],
    [State('recordsname', 'value')],
    [State('recordsdate', 'start_date')],
    [State('recordsdate', 'end_date')],
    [State('recordsoppo', 'value')],
    [State('recordssurface', 'value')],
    [State('recordsmatch', 'value')],
    [State('recordsround', 'value')],
    [State('recordsresult', 'value')],
    [State('recordsstreak', 'value')],
    [State('recordslayout', 'value')],
)
def update_records(state, name, start, end, oppo, surface, match, round, result, streak, layout):
    data = records(name, [start, end], oppo, surface, match, round, result, streak, layout)
    return data
