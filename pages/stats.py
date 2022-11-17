# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import html, dcc, dash_table
import dash
import plotly.express as px
import pandas as pd
import plotly.figure_factory as ff
import numpy as np
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from datetime import date as dt
from dash.exceptions import PreventUpdate

# get all names
all_names = []
with open('mwplayerlist_processed.txt', 'r') as f:
    for line in f:
        all_names.append(line[:-1])

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

# titles
def titles(names, mode, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']
    atp1000 = ['Indian Wells Masters', 'Miami Masters', 'Monte Carlo Masters', 'Madrid Masters', 'Rome Masters', 'Canada Masters', 'Cincinnati Masters', 'Shanghai Masters', 'Paris Masters', 'Hamburg Masters']
    
    fig = go.Figure()

    if mode == 'all':
        attri = ['GS', 'ATP1000', 'ATP Finale', 'Olympics', 'All']
        for i, name in enumerate(names):
            counts = []
            # gs
            counts.append(len(dfs[i][(dfs[i]['Tournament'].isin(gs)) & (dfs[i]['Rd'] == 'F') & (dfs[i]['W'] == 1)]))
            # atp1000
            counts.append(len(dfs[i][(dfs[i]['Tournament'].isin(atp1000)) & (dfs[i]['Rd'] == 'F') & (dfs[i]['W'] == 1)]))
            # atp final
            counts.append(len(dfs[i][(dfs[i]['Tournament'].isin(['Tour Finals', 'Masters Cup'])) & (dfs[i]['Rd'] == 'F') & (dfs[i]['W'] == 1)]))
            # olympics
            counts.append(len(dfs[i][(dfs[i]['Tournament'].str.contains('Olympics')) & (dfs[i]['Rd'] == 'F') & (dfs[i]['W'] == 1)]))
            # sum of all
            counts.append(sum(counts))

            fig.add_trace(go.Bar(
                x = attri,
                y = counts,
                name = name[4:],
                text = counts,
            ))

    elif mode == 'gs':
        for i, name in enumerate(names):
            counts = []
            for g in gs:
                counts.append(len(dfs[i][(dfs[i]['Tournament'] == g) & (dfs[i]['Rd'] == 'F') & (dfs[i]['W'] == 1)]))
            counts.append(sum(counts))

            fig.add_trace(go.Bar(
                x = gs + ['All'],
                y = counts,
                name = name[4:],
                text = counts,
            ))

    elif mode == 'atp1000':
        for i, name in enumerate(names):
            counts = []
            for a in atp1000:
                counts.append(len(dfs[i][(dfs[i]['Tournament'] == a) & (dfs[i]['Rd'] == 'F') & (dfs[i]['W'] == 1)]))
            counts.append(sum(counts))

            fig.add_trace(go.Bar(
                x = atp1000 + ['All'],
                y = counts,
                name = name[4:],
                text = counts,
            ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(
        title_text = 'Champion Titles ' + datetext,
        xaxis_title = 'Tournaments',
        yaxis_title = 'Counts',
        showlegend = True,
        template = 'plotly_dark',
    )

    return fig

# h2h
def h2h(names, date = [None, None]):
    df = clean_df(load_txt(names[0]), date)
    attrs = ['All', 'GS', 'Hard', 'Grass', 'Clay']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']
    p1 = []
    p2 = []
    # all h2h
    p1.append(len(df[(df['WP'] ==  names[0][4:]) & (df['LP'] ==  names[1][4:])]))
    p2.append(len(df[(df['LP'] ==  names[0][4:]) & (df['WP'] ==  names[1][4:])]))
    # gs
    p1.append(len(df[(df['WP'] ==  names[0][4:]) & (df['LP'] ==  names[1][4:]) & (df['Tournament'].isin(gs))]))
    p2.append(len(df[(df['LP'] ==  names[0][4:]) & (df['WP'] ==  names[1][4:]) & (df['Tournament'].isin(gs))]))
    # hard
    p1.append(len(df[(df['WP'] ==  names[0][4:]) & (df['LP'] ==  names[1][4:]) & (df['Surface'] == 'Hard')]))
    p2.append(len(df[(df['LP'] ==  names[0][4:]) & (df['WP'] ==  names[1][4:]) & (df['Surface'] == 'Hard')]))
    # grass
    p1.append(len(df[(df['WP'] ==  names[0][4:]) & (df['LP'] ==  names[1][4:]) & (df['Surface'] == 'Grass')]))
    p2.append(len(df[(df['LP'] ==  names[0][4:]) & (df['WP'] ==  names[1][4:]) & (df['Surface'] == 'Grass')]))
    # clay
    p1.append(len(df[(df['WP'] ==  names[0][4:]) & (df['LP'] ==  names[1][4:]) & (df['Surface'] == 'Clay')]))
    p2.append(len(df[(df['LP'] ==  names[0][4:]) & (df['WP'] ==  names[1][4:]) & (df['Surface'] == 'Clay')]))

    fig = go.Figure()

    for i, p in enumerate([p1, p2]):
        fig.add_trace(go.Bar(
            x = attrs,
            y = p,
            width = [0.3 for i in range(5)],
            text = p,
            name = names[i][4:]
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(
        title_text = 'Head 2 Head ' + datetext,
        xaxis_title = 'Tournament/Surface',
        yaxis_title = 'Win Counts',
        template = 'plotly_dark',
    )

    return fig

# moving average winning ratio
def mawr(names, num = 100):
    dfs = [clean_df(load_txt(name)) for name in names]
    fig = px.line()
    for i, name in enumerate(names):
        wr = []
        for j in range(len(dfs[i]) - (num - 1)):
            wr.append(sum(dfs[i]['W'][(len(dfs[i]) - j - num):(len(dfs[i]) - j)]) / num)
        dates = [dfs[i]['Date'][((len(dfs[i]) - j - num) + (len(dfs[i]) - j - 1)) // 2] for j in range(len(dfs[i]) - (num - 1))]
        fig.add_scatter(x = dates, y = wr, name = name[4:])
    fig.update_layout(
        title_text = 'Moving Average Winning Ratio per ' + str(num) + ' Matches',
        xaxis_title = 'Date',
        yaxis_title = 'Winning Ratio',
        showlegend = True,
        template = 'plotly_dark',
    )

    return fig

# ace rate
def ace(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    a_data = [df["A%"][~np.isnan(df['A%'])] for df in dfs]
    a_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(a_data, a_labels, bin_size = .5)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'Ace Rate ' + datetext,
                        xaxis_title = "Ace (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                        )
    return fig

# doublef rate
def doublef(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    a_data = [df["DF%"][~np.isnan(df['DF%'])] for df in dfs]
    a_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(a_data, a_labels, bin_size = .2)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'Double Fault Rate ' + datetext,
                        xaxis_title = "Double Fault (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# 1stIn
def fsi(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    fsi_data = [df["1stIn"][~np.isnan(df['1stIn'])] for df in dfs]
    fsi_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(fsi_data, fsi_labels, bin_size = .5)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = '1stServe-In Rate ' + datetext,
                        xaxis_title = "1stIn (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# 1st%
def fsw(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    fsw_data = [df["1st%"][~np.isnan(df['1st%'])] for df in dfs]
    fsw_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(fsw_data, fsw_labels, bin_size = .5)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = '1stServe Win % ' + datetext,
                        xaxis_title = "First Serve Point Win (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# 2nd%
def ssw(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    ssw_data = [df["2nd%"][~np.isnan(df['2nd%'])] for df in dfs]
    ssw_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(ssw_data, ssw_labels, bin_size = 2)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = '2ndServe Win% ' + datetext,
                        xaxis_title = "Second Serve Point Win (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# dr
def dr(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    dr_data = [df["DR"][~np.isnan(df['DR'])] for df in dfs]
    dr_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(dr_data, dr_labels, bin_size = .05)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'Dominance Rate ' + datetext,
                        xaxis_title = "DR",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# TPW
def tpw(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    tpw_data = [df["TPW"][~np.isnan(df['TPW'])] for df in dfs]
    tpw_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(tpw_data, tpw_labels, bin_size = .5)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'TPW ' + datetext,
                        xaxis_title = "TPW (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# RPW
def rpw(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    rpw_data = [df["RPW"][~np.isnan(df['RPW'])] for df in dfs]
    rpw_labels = [name[4:] for name in names]
    try:
        fig = ff.create_distplot(rpw_data, rpw_labels, bin_size = .5)
    except:
        fig = go.Figure()
    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'RPW ' + datetext,
                        xaxis_title = "RPW (Percent)",
                        yaxis_title = "Density",
                        template = 'plotly_dark',
                    )
    return fig

# bpgive
def bpgive(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['All', 'GS', 'Finals', 'Hard', 'Grass', 'Clay']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']

    fig = go.Figure()

    for i, name in enumerate(names):
        perc = []
        # All
        df_s = dfs[i]
        sp = sum(df_s['SP'][~df_s['SP'].isna()])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        try:
            perc.append(bp * 100 / sp)
        except:
            perc.append('')
        # GS
        df_s = dfs[i][dfs[i]['Tournament'].isin(gs)]
        sp = sum(df_s['SP'][~df_s['SP'].isna()])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        try:
            perc.append(bp * 100 / sp)
        except:
            perc.append('')
        # Finals
        df_s = dfs[i][dfs[i]['Rd'] == 'F']
        sp = sum(df_s['SP'][~df_s['SP'].isna()])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        try:
            perc.append(bp * 100 / sp)
        except:
            perc.append('')
        # Hard, Grass, Clay
        for s in ['Hard', 'Grass', 'Clay']:
            df_s = dfs[i][dfs[i]['Surface'] == s]
            sp = sum(df_s['SP'][~df_s['SP'].isna()])
            bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
            try:
                perc.append(bp * 100 / sp)
            except:
                perc.append('')

        fig.add_trace(go.Bar(
            x = attrs,
            y = perc,
            name = name[4:],
            text = [str(p)[:4] + '%' for p in perc],
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'BPGiven / TSP ' + datetext,
                        xaxis_title = "Scenarios",
                        yaxis_title = "Percent",
                        template = 'plotly_dark',
                        showlegend = True,
                        yaxis_range = [0, 100],
                    )
    return fig

# bps
def bps(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['All', 'GS', 'Finals', 'Hard', 'Grass', 'Clay']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']

    fig = go.Figure()

    for i, name in enumerate(names):
        perc = []
        # All
        df_s = dfs[i]
        bpsvd = sum([int(r.split('/')[0]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        try:
            perc.append(bpsvd * 100 / bp)
        except:
            perc.append('')
        # GS
        df_s = dfs[i][dfs[i]['Tournament'].isin(gs)]
        bpsvd = sum([int(r.split('/')[0]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        try:
            perc.append(bpsvd * 100 / bp)
        except:
            perc.append('')
        # Finals
        df_s = dfs[i][dfs[i]['Rd'] == 'F']
        bpsvd = sum([int(r.split('/')[0]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
        try:
            perc.append(bpsvd * 100 / bp)
        except:
            perc.append('')
        # Hard, Grass, Clay
        for s in ['Hard', 'Grass', 'Clay']:
            df_s = dfs[i][dfs[i]['Surface'] == s]
            bpsvd = sum([int(r.split('/')[0]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
            bp = sum([int(r.split('/')[1]) for r in df_s['BPSvd'][~df_s['BPSvd'].isna()]])
            try:
                perc.append(bpsvd * 100 / bp)
            except:
                perc.append('')

        fig.add_trace(go.Bar(
            x = attrs,
            y = perc,
            name = name[4:],
            text = [str(p)[:4] + '%' for p in perc],
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'BPSaved / BPGiven ' + datetext,
                        xaxis_title = "Scenarios",
                        yaxis_title = "Percent",
                        template = 'plotly_dark',
                        showlegend = True,
                        yaxis_range = [0, 100],
                    )
    return fig

# bpget
def bpget(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['All', 'GS', 'Finals', 'Hard', 'Grass', 'Clay']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']

    fig = go.Figure()

    for i, name in enumerate(names):
        perc = []
        # All
        df_s = dfs[i]
        rp = sum(df_s['TP'][~np.isnan(df_s['TP'])] - df_s['SP'][~df_s['SP'].isna()])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        try:
            perc.append(bp * 100 / rp)
        except:
            perc.append('')
        # GS
        df_s = dfs[i][dfs[i]['Tournament'].isin(gs)]
        rp = sum(df_s['TP'][~np.isnan(df_s['TP'])] - df_s['SP'][~df_s['SP'].isna()])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        try:
            perc.append(bp * 100 / rp)
        except:
            perc.append('')
        # Finals
        df_s = dfs[i][dfs[i]['Rd'] == 'F']
        rp = sum(df_s['TP'][~np.isnan(df_s['TP'])] - df_s['SP'][~df_s['SP'].isna()])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        try:
            perc.append(bp * 100 / rp)
        except:
            perc.append('')
        # Hard, Grass, Clay
        for s in ['Hard', 'Grass', 'Clay']:
            df_s = dfs[i][dfs[i]['Surface'] == s]
            rp = sum(df_s['TP'][~np.isnan(df_s['TP'])] - df_s['SP'][~df_s['SP'].isna()])
            bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
            try:
                perc.append(bp * 100 / rp)
            except:
                perc.append('')

        fig.add_trace(go.Bar(
            x = attrs,
            y = perc,
            name = name[4:],
            text = [str(p)[:4] + '%' for p in perc],
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'BPGot / TRP ' + datetext,
                        xaxis_title = "Scenarios",
                        yaxis_title = "Percent",
                        template = 'plotly_dark',
                        showlegend = True,
                        yaxis_range = [0, 100],
                    )
    return fig

# bpc
def bpc(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['All', 'GS', 'Finals', 'Hard', 'Grass', 'Clay']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']

    fig = go.Figure()

    for i, name in enumerate(names):
        perc = []
        # All
        df_s = dfs[i]
        bpcnv = sum([int(r.split('/')[0]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        try:
            perc.append(bpcnv * 100 / bp)
        except:
            perc.append('')
        # GS
        df_s = dfs[i][dfs[i]['Tournament'].isin(gs)]
        bpcnv = sum([int(r.split('/')[0]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        try:
            perc.append(bpcnv * 100 / bp)
        except:
            perc.append('')
        # Finals
        df_s = dfs[i][dfs[i]['Rd'] == 'F']
        bpcnv = sum([int(r.split('/')[0]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
        try:
            perc.append(bpcnv * 100 / bp)
        except:
            perc.append('')
        # Hard, Grass, Clay
        for s in ['Hard', 'Grass', 'Clay']:
            df_s = dfs[i][dfs[i]['Surface'] == s]
            bpcnv = sum([int(r.split('/')[0]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
            bp = sum([int(r.split('/')[1]) for r in df_s['BPCnv'][~df_s['BPCnv'].isna()]])
            try:
                perc.append(bpcnv * 100 / bp)
            except:
                perc.append('')

        fig.add_trace(go.Bar(
            x = attrs,
            y = perc,
            name = name[4:],
            text = [str(p)[:4] + '%' for p in perc],
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'BPCnv / BPGot ' + datetext,
                        xaxis_title = "Scenarios",
                        yaxis_title = "Percent",
                        template = 'plotly_dark',
                        showlegend = True,
                        yaxis_range = [0, 100],
                    )
    return fig

# win lose counts
def wlc(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['CareerWin', 'CareerLoss', 'GsWin', 'GsLoss']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']
    fig = go.Figure()

    for i, name in enumerate(names):
        cnt = [len(dfs[i][dfs[i]['W'] == 1]), len(dfs[i][dfs[i]['W'] == 0]), len(dfs[i][(dfs[i]['W'] == 1) & (dfs[i]['Tournament'].isin(gs))]), len(dfs[i][(dfs[i]['W'] == 0) & (dfs[i]['Tournament'].isin(gs))])]
        fig.add_trace(go.Bar(
            x = attrs,
            y = cnt,
            name = name[4:],
            text = cnt,
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'Wins vs Losses ' + datetext,
                        xaxis_title = "Results",
                        yaxis_title = "Counts",
                        template = 'plotly_dark',
                        showlegend = True,
                    )
    return fig

# gs win lose counts
def gswlc(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['WC-Win', 'WC-Loss', 'USO-Win', 'USO-Loss', 'AO-Win', 'AO-Loss', 'FO-Win', 'FO-Loss']
    gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']
    fig = go.Figure()

    for i, name in enumerate(names):
        cnt = []
        for item in gs:
            cnt.append((len(dfs[i][(dfs[i]['Tournament'] == item) & (dfs[i]['W'] == 1)])))
            cnt.append((len(dfs[i][(dfs[i]['Tournament'] == item) & (dfs[i]['W'] == 0)])))
        fig.add_trace(go.Bar(
            x = attrs,
            y = cnt,
            name = name[4:],
            text = cnt,
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'GS Wins vs GS Losses ' + datetext,
                        xaxis_title = "Results",
                        yaxis_title = "Counts",
                        template = 'plotly_dark',
                        showlegend = True,
                    )
    return fig

# bigheart
def bigheart(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['Lose 1 -> Win 2', 'Lose 2 -> Win 3']

    fig = go.Figure()

    for i, name in enumerate(names):
        cnt = [0,0]
        # lose 1 -> win 2
        for r in dfs[i][(dfs[i]['W'] == 1) & (dfs[i]['Sets'] == 3)]['Score']:
            try:
                res = r.split(' ')
                if (int(res[0][0]) < int(res[0][2])) and ('RET' not in res):
                    cnt[0] += 1
            except:
                pass
        # lose 2 -> win 3
        for r in dfs[i][(dfs[i]['W'] == 1) & (dfs[i]['Sets'] == 5)]['Score']:
            try:
                res = r.split(' ')
                if (int(res[0][0]) < int(res[0][2])) and (int(res[1][0]) < int(res[1][2])) and ('RET' not in res):
                    cnt[1] += 1
            except:
                pass
        
        fig.add_trace(go.Bar(
            x = attrs,
            y = cnt,
            name = name[4:],
            text = cnt,
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'Big Heart Matches ' + datetext,
                        xaxis_title = "Scenarios",
                        yaxis_title = "Win Counts",
                        template = 'plotly_dark',
                        showlegend = True,
                    )
    return fig

# crystalheart
def crystalheart(names, date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    attrs = ['Win 1 -> Lose 2', 'Win 2 -> Lose 3']

    fig = go.Figure()

    for i, name in enumerate(names):
        cnt = [0,0]
        # Win 1 -> Lose 2
        for r in dfs[i][(dfs[i]['W'] == 0) & (dfs[i]['Sets'] == 3)]['Score']:
            try:
                res = r.split(' ')
                if (int(res[0][0]) < int(res[0][2])) and ('RET' not in res):
                    cnt[0] += 1
            except:
                pass
        # Win 2 -> Lose 3
        for r in dfs[i][(dfs[i]['W'] == 0) & (dfs[i]['Sets'] == 5)]['Score']:
            try:
                res = r.split(' ')
                if (int(res[0][0]) < int(res[0][2])) and (int(res[1][0]) < int(res[1][2])) and ('RET' not in res):
                    cnt[1] += 1
            except:
                pass
        
        fig.add_trace(go.Bar(
            x = attrs,
            y = cnt,
            name = name[4:],
            text = cnt,
        ))

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = 'Crystal Heart Matches ' + datetext,
                        xaxis_title = "Scenarios",
                        yaxis_title = "Lose Counts",
                        template = 'plotly_dark',
                        showlegend = True,
                    )
    return fig

# define serve stats function
def serve(names, mode, date = [None, None]):
    if mode == 'ace':
        return ace(names, date)
    elif mode == 'doublef':
        return doublef(names, date)
    elif mode == 'fsi':
        return fsi(names, date)
    elif mode == 'fsw':
        return fsw(names, date)
    elif mode == 'ssw':
        return ssw(names, date)

# define point stats function
def point(names, mode, date = [None, None]):
    if mode == 'dr':
        return dr(names, date)
    elif mode == 'tpw':
        return tpw(names, date)
    elif mode == 'rpw':
        return rpw(names, date)

# define break points function
def bp(names, mode, date = [None, None]):
    if mode == 'bpgive':
        return bpgive(names, date)
    elif mode == 'bps':
        return bps(names, date)
    elif mode == 'bpget':
        return bpget(names, date)
    elif mode == 'bpc':
        return bpc(names, date)

# define thrilling matches function
def thrill(names, mode, date = [None, None]):
    if mode == 'wlc':
        return wlc(names, date)
    elif mode == 'gswlc':
        return gswlc(names, date)
    elif mode == 'bigheart':
        return bigheart(names, date)
    elif mode == 'crystalheart':
        return crystalheart(names, date)

# define a conprehensive wrtp functions to consider all surfaces
def wrtpsurface(names, final = 'No', surface = ['Hard', 'Grass', 'Clay'], date = [None, None]):
    # selection - surface: hard, grass, clay, all
    # selection - final: yes, no
    dfs = [clean_df(load_txt(name), date) for name in names]
    dic = {}
    for name in names:
        dic[name[4:]] = []
    rks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000]

    if final == 'Yes':
        for rk in rks:
            for i, name in enumerate(names):
                try:
                    dic[name[4:]].append(len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['W'] == 1) & (dfs[i]['Surface'].isin(surface)) & (dfs[i]['Rd'] == 'F')]) / len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['Surface'].isin(surface)) & (dfs[i]['Rd'] == 'F')]))
                except:
                    dic[name[4:]].append(np.nan)
    else:
        for rk in rks:
            for i, name in enumerate(names):
                try:
                    dic[name[4:]].append(len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['W'] == 1) & (dfs[i]['Surface'].isin(surface))]) / len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['Surface'].isin(surface))]))
                except:
                    dic[name[4:]].append(np.nan)

    df = pd.DataFrame(dic, index = rks)
    fig = px.line(df, x = df.index, y = [name[4:] for name in names], markers = True)

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = "WR by Surface " + datetext,
                        xaxis_title = 'Top X Player',
                        yaxis_title = 'Winning Ratio',
                        template = 'plotly_dark',
                        yaxis_range = [0, 1],
                    )
    return fig

# define a conprehensive wrtp functions to consider important tournaments
def wrtptournament(names, final = 'No', tournament = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros'], date = [None, None]):
    # selection - surface: hard, grass, clay, all
    # selection - final: yes, no
    dfs = [clean_df(load_txt(name), date) for name in names]
    dic = {}
    for name in names:
        dic[name[4:]] = []
    rks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 150, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1500, 2000]
    atp1000 = ['Indian Wells Masters', 'Miami Masters', 'Monte Carlo Masters', 'Madrid Masters', 'Rome Masters', 'Canada Masters', 'Cincinnati Masters', 'Shanghai Masters', 'Paris Masters', 'Hamburg Masters']

    if final == 'Yes':
        if 'ATP1000' in tournament:
            for rk in rks:
                for i, name in enumerate(names):
                    try:
                        dic[name[4:]].append(len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['W'] == 1) & (dfs[i]['Tournament'].isin(tournament + atp1000)) & (dfs[i]['Rd'] == 'F')]) / len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['Tournament'].isin(tournament + atp1000)) & (dfs[i]['Rd'] == 'F')]))
                    except:
                        dic[name[4:]].append(np.nan)
        else:
            for rk in rks:
                for i, name in enumerate(names):
                    try:
                        dic[name[4:]].append(len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['W'] == 1) & (dfs[i]['Tournament'].isin(tournament)) & (dfs[i]['Rd'] == 'F')]) / len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['Tournament'].isin(tournament)) & (dfs[i]['Rd'] == 'F')]))
                    except:
                        dic[name[4:]].append(np.nan)
    else:
        if 'ATP1000' in tournament:
            for rk in rks:
                for i, name in enumerate(names):
                    try:
                        dic[name[4:]].append(len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['W'] == 1) & (dfs[i]['Tournament'].isin(tournament + atp1000))]) / len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['Tournament'].isin(tournament + atp1000))]))
                    except:
                        dic[name[4:]].append(np.nan)
        else:
            for rk in rks:
                for i, name in enumerate(names):
                    try:
                        dic[name[4:]].append(len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['W'] == 1) & (dfs[i]['Tournament'].isin(tournament))]) / len(dfs[i][(dfs[i]['vRk'] <= rk) & (dfs[i]['Tournament'].isin(tournament))]))
                    except:
                        dic[name[4:]].append(np.nan)

    df = pd.DataFrame(dic, index = rks)
    fig = px.line(df, x = df.index, y = [name[4:] for name in names], markers = True)

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = "WR by Tournment " + datetext,
                        xaxis_title = 'Top X Player',
                        yaxis_title = 'Winning Ratio',
                        template = 'plotly_dark',
                        yaxis_range = [0, 1],
                        )
    return fig

# winning rate at different rounds of GS
def wrgsr(names, gs = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros'], date = [None, None]):
    dfs = [clean_df(load_txt(name), date) for name in names]
    dic = {}
    for name in names:
        dic[name[4:]] = []
    rds = ['R128', 'R64', 'R32', 'R16', 'QF', 'SF', 'F']

    for rd in rds:
        for i, name in enumerate(names):
            try:
                dic[name[4:]].append(len(dfs[i][(dfs[i]['Tournament'].isin(gs)) & (dfs[i]['W'] == 1) & (dfs[i]['Rd'] == rd)]) / len(dfs[i][(dfs[i]['Tournament'].isin(gs)) & (dfs[i]['Rd'] == rd)]))
            except:
                dic[name[4:]].append(np.nan)

    df = pd.DataFrame(dic, index = rds)
    fig = px.line(df, x = df.index, y = [name[4:] for name in names], markers = True)

    datetext = ''
    if date != [None, None]:
        if date[0] == None:
            datetext = '- (past ~ ' + date[1] + ')'
        elif date[1] == None:
            datetext = '- (' + date[0] + ' ~ now)'
        else:
            datetext = '- (' + date[0] + ' ~ ' + date[1] + ')'

    fig.update_layout(title_text = "WR at GS Rounds " + datetext,
                        xaxis_title = 'Round',
                        yaxis_title = 'Winning Ratio',
                        template = 'plotly_dark',
                        yaxis_range = [0, 1],
                    )
    return fig

# create page
dash.register_page(__name__, name = 'Stats Visualization')

layout = html.Div(children=[

    # head
    html.Div(children=[
        html.H2('Enter players\' names for stats visual comparison:'),
        dcc.Dropdown(id="nameinput", placeholder = 'Enter Player Name:', search_value = '(M) Novak Djokovic', value = ['(M) Novak Djokovic'], multi = True, style = {'color': 'grey', 'background-color': 'rgb(17,17,17)'}),
        html.Br(),
        # selecr career or date
        html.Div(children=[
            dcc.RadioItems(id="careerdate", options = ['All Career', 'By Date'], value = 'All Career', style = {'display': 'inline-block'},),
            dcc.DatePickerRange(id="selectdate",
                start_date_placeholder_text = 'Start Date',
                end_date_placeholder_text = 'End Date',
                style = {'display': 'inline-block'},
            ),
        ]),
        html.Br(),
        html.Button("Search", id='confirm', n_clicks = 0, style = {'font-size': '25px', 'color': 'gold', 'background-color': 'rgb(17,17,17)', 'border-radius': '12px', 'border-color': 'gold', 'cursor': 'pointer'}),
    ],
    ),

    # section for titles and H2H
    html.Div(children=[
        # titles figure
        html.Div(children=[
            html.Br(),
            dcc.Tabs(id="titlestabs", value='all', children=[
                dcc.Tab(label='Titles Overview', value='all', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='Grand Slam', value='gs', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='ATP1000', value='atp1000', className='tab_style', selected_className='tab_selected_style'),
            ], className='tabs_styles'),
            dcc.Graph(id='titles', figure = titles(['(M) Novak Djokovic'], 'all')),
        ], className = 'column2'
        ),

        # h2h figure
        html.Div(children=[
            html.Br(),
            html.Div(children=[
                dcc.Dropdown(id="h2hinput1", search_value = '(M) Novak Djokovic',  value = '(M) Novak Djokovic', clearable = False, style = {'background-color': 'rgb(17,17,17)'}),
                dcc.Dropdown(id="h2hinput2", search_value = '(M) Rafael Nadal', value = '(M) Rafael Nadal', clearable = False, style = {'background-color': 'rgb(17,17,17)'}),
            ]
            ),
            dcc.Graph(id='h2h', figure = h2h(['(M) Novak Djokovic', '(M) Rafael Nadal'])),
        ], className = 'column2'
        )
    ], className = 'row2',
    ),

    # section for moving average winning
    html.Div(children=[
            html.Br(style = {'display': 'block', 'size' : '1px'}),
            dcc.Slider(0, 200, 10, value=100, id='mawrslider'),
            dcc.Graph(id='mawr', figure = mawr(['(M) Novak Djokovic'])),
        ], style={'color': 'gold', 'background': 'rgb(17,17,17)'}
        ),

    # section for serves and ponits stats
    html.Div(children=[
        # serve stats
        html.Div(children=[
            html.Br(),
            dcc.Tabs(id="servetabs", value='ace', children=[
                dcc.Tab(label='Ace', value='ace', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='Double Fault', value='doublef', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='1st Serve In', value='fsi', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='1st Serve Pts Win', value='fsw', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='2nd Serve Pts Win', value='ssw', className='tab_style', selected_className='tab_selected_style'),
            ], className='tabs_styles'),
            dcc.Graph(id='serve', figure = serve(['(M) Novak Djokovic'], 'ace')),
        ], className = 'column2'
        ),
        # point stats
        html.Div(children=[
            html.Br(),
            dcc.Tabs(id="pointtabs", value='dr', children=[
                dcc.Tab(label='Dominance Rate', value='dr', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='Total Points Win', value='tpw', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='Return Points Win', value='rpw', className='tab_style', selected_className='tab_selected_style'),
            ], className='tabs_styles'),
            dcc.Graph(id='point', figure = point(['(M) Novak Djokovic'], 'dr')),
        ], className = 'column2'
        ),
    ], className = 'row2'
    ),

    # section for break points and thrilling matches
    html.Div(children=[
        # break points stats
        html.Div(children=[
            html.Br(),
            dcc.Tabs(id="bptabs", value='bpgive', children=[
                dcc.Tab(label='BPGiven', value='bpgive', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='BPSvd', value='bps', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='BPGot', value='bpget', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='BPCnv', value='bpc', className='tab_style', selected_className='tab_selected_style'),
            ], className='tabs_styles'),
            dcc.Graph(id='bp', figure = bp(['(M) Novak Djokovic'], 'bpgive')),
        ], className = 'column2'
        ),
        # thrilling matches
        html.Div(children=[
            html.Br(),
            dcc.Tabs(id="thrilltabs", value='wlc', children=[
                dcc.Tab(label='Wins vs Losses', value='wlc', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='GS Wins vs GS Losses', value='gswlc', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='Big Heart Matches', value='bigheart', className='tab_style', selected_className='tab_selected_style'),
                dcc.Tab(label='Crystal Heart Matches', value='crystalheart', className='tab_style', selected_className='tab_selected_style'),
            ], className='tabs_styles'),
            dcc.Graph(id='thrill', figure = thrill(['(M) Novak Djokovic'], 'wlc')),
        ], className = 'column2'
        ),
    ], className = 'row2'
    ),

    # section for winning ratios
    html.Div(children=[
        # wr surface figure
        html.Div(
            children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Label('Final', className = 'label'),
                        dcc.RadioItems(id="finalsurface", options = ['Yes', 'No'], value = 'No'),
                    ], style={'display': 'inline-block', 'width': '20%', 'min-width': '120px', 'padding': '10px'}
                    ),
                    html.Div(children=[
                        html.Label('Surface', className = 'label'),
                        dcc.Checklist(id="surface", options = ["Hard", "Grass", "Clay"], value = ["Hard", "Grass", "Clay"]),
                    ], style={'display': 'inline-block', 'width': '70%', 'padding': '10px'}
                    )
                    ], className = 'selection-area'
                ), 
                html.Br(),
                dcc.Graph(id='wrtpsurface', figure = wrtpsurface(['(M) Novak Djokovic'])),
            ], style={'color': 'gold', 'background': 'rgb(17,17,17)'}, className='column3',
        ),
        # wr tournament figure
        html.Div(
            children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Label('Final', className = 'label'),
                        dcc.RadioItems(id="finaltournament", options = ['Yes', 'No'], value = 'No'),
                    ], style={'display': 'inline-block', 'width': '20%', 'min-width': '120px', 'padding': '10px'}
                    ),
                    html.Div(children=[
                        html.Label('Tournament', className = 'label'),
                        dcc.Checklist(id="tournament", options = {'Wimbledon': 'WC', 'US Open': 'USO', 'Australian Open': 'AO', 'Roland Garros': 'FO', 'ATP1000': 'ATP1000'}, value = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']),
                    ], style={'display': 'inline-block', 'width': '70%', 'min-width': '300px', 'padding': '10px'}
                    ),
                ], className = 'selection-area'
                ),
                html.Br(),
                dcc.Graph(id='wrtptournament', figure = wrtptournament(['(M) Novak Djokovic'])),
            ], style={'color': 'gold', 'background': 'rgb(17,17,17)'}, className='column3',
        ),
        # section for gsr
        html.Div(
            children=[
                html.Div(children=[
                    html.Div(children=[
                        html.Label('Grand Slam', className = 'label'),
                        dcc.Checklist(id="gs", options = {'Wimbledon': 'WC', 'US Open': 'USO', 'Australian Open': 'AO', 'Roland Garros': 'FO'}, value = ['Wimbledon', 'US Open', 'Australian Open', 'Roland Garros']),
                    ], style={'display': 'inline-block', 'padding': '10px'}
                    ),
                ], className = 'selection-area'
                ),
                html.Br(),
                dcc.Graph(id='wrgsr', figure = wrgsr(['(M) Novak Djokovic'])),
            ], style={'color': 'gold', 'background': 'rgb(17,17,17)'}, className='column3',
        )
    ], style={'background': 'rgb(17,17,17)'}, className='row3'
    ),
])

# update nameinput options
@dash.callback(
    Output("nameinput", "options"),
    Input("nameinput", "search_value"),
    State("nameinput", "value")
)
def update_nameinput_options(search_value, value):
    if not search_value:
        raise PreventUpdate
    # Make sure that the set values are in the option list, else they will disappear
    # from the shown select list, but still part of the `value`.
    return [
        o for o in all_names if search_value.lower() in o.lower() or o.lower() in ([v.lower() for v in value] or [])
    ]

# update h2hinput options
@dash.callback(
    Output("h2hinput1", "options"),
    Input("h2hinput1", "search_value")
)
def update_h2hinput1_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in all_names if search_value.lower() in o.lower()]

@dash.callback(
    Output("h2hinput2", "options"),
    Input("h2hinput2", "search_value")
)
def update_h2hinput2_options(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in all_names if search_value.lower() in o.lower()]

# career or date
@dash.callback(
    [Output('selectdate', 'disabled'), Output('selectdate', 'start_date'), Output('selectdate', 'end_date')],
    [Input('careerdate', 'value')],
)

def career_or_date(mode):
    if mode == 'All Career':
        return True, None, None
    elif mode == 'By Date':
        return False, None, None

# titles
@dash.callback(
    Output('titles', 'figure'),
    [Input('confirm', 'n_clicks')],
    [Input('titlestabs', 'value')],
    [State('nameinput', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_titles(state, mode, input, start, end):
    try:
        fig = titles(input, mode, [start, end])
    except:
        fig = titles([input], mode, [start, end])
    return fig

# h2h
@dash.callback(
    Output('h2h', 'figure'),
    [Input('confirm', 'n_clicks')],
    [Input('h2hinput1', 'value')],
    [Input('h2hinput2', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_h2h(state, input1, input2, start, end):
    fig = h2h([input1, input2], [start, end])
    return fig

# mawr
@dash.callback(
    Output('mawr', 'figure'),
    [Input('confirm', 'n_clicks')],
    [State('nameinput', 'value')],
    [Input('mawrslider', 'value')],
)
def update_mawr(state, input, slide):
    try:
        fig = mawr(input, slide)
    except:
        fig = mawr([input], slide)
    return fig

# serve
@dash.callback(
    Output('serve', 'figure'),
    [Input('confirm', 'n_clicks')],
    [Input('servetabs', 'value')],
    [State('nameinput', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_serve(state, mode, input, start, end):
    try:
        fig = serve(input, mode, [start, end])
    except:
        fig = serve([input], mode, [start, end])
    return fig

# point
@dash.callback(
    Output('point', 'figure'),
    [Input('confirm', 'n_clicks')],
    [Input('pointtabs', 'value')],
    [State('nameinput', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_point(state, mode, input, start, end):
    try:
        fig = point(input, mode, [start, end])
    except:
        fig = point([input], mode, [start, end])
    return fig

# break points
@dash.callback(
    Output('bp', 'figure'),
    [Input('confirm', 'n_clicks')],
    [Input('bptabs', 'value')],
    [State('nameinput', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_bp(state, mode, input, start, end):
    try:
        fig = bp(input, mode, [start, end])
    except:
        fig = bp([input], mode, [start, end])
    return fig

# thrilling matches
@dash.callback(
    Output('thrill', 'figure'),
    [Input('confirm', 'n_clicks')],
    [Input('thrilltabs', 'value')],
    [State('nameinput', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_thrill(state, mode, input, start, end):
    try:
        fig = thrill(input, mode, [start, end])
    except:
        fig = thrill([input], mode, [start, end])
    return fig

# wrtpsurface
@dash.callback(
    Output('wrtpsurface', 'figure'),
    [Input('confirm', 'n_clicks')],
    [State('nameinput', 'value')],
    [Input('finalsurface', 'value')],
    [Input('surface', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_wrtpsurface(state, input, final, surface, start, end):
    try:
        fig = wrtpsurface(input, final, surface, [start, end])
    except:
        fig = wrtpsurface([input], final, surface, [start, end])
    return fig

# wrtptournament
@dash.callback(
    Output('wrtptournament', 'figure'),
    [Input('confirm', 'n_clicks')],
    [State('nameinput', 'value')],
    [Input('finaltournament', 'value')],
    [Input('tournament', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_wrtptournament(state, input, final, surface, start, end):
    try:
        fig = wrtptournament(input, final, surface, [start, end])
    except:
        fig = wrtptournament([input], final, surface, [start, end])
    return fig

# wrgsr
@dash.callback(
    Output('wrgsr', 'figure'),
    [Input('confirm', 'n_clicks')],
    [State('nameinput', 'value')],
    [Input('gs', 'value')],
    [State('selectdate', 'start_date')],
    [State('selectdate', 'end_date')]
)
def update_wrgsr(state, input, gs, start, end):
    try:
        fig = wrgsr(input, gs, [start, end])
    except:
        fig = wrgsr([input], gs, [start, end])
    return fig