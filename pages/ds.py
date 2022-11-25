# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

# load txt files
def load_txt(file):
    with open(file, 'r', encoding='utf-8-sig') as f:
        attributes = f.readline()[:-1].split(',')
        df = pd.DataFrame([line[:-1].split(',') for line in f], columns = attributes)
    f.close()
    return df

# load ds file
df = load_txt('m/ds/atpdsselected.txt')
attrs = ['Weight (kg)', 'Height (cm)', 'Right-Left-Handed', 'Two-One-Backhanded', 'Matches', 'Wins', 'Losses', 'Winning Ratio', 'Ace (%)', 'Double Fault (%)', '1st Serve In (%)', '1st Serve Win (%)', '2nd Serve Win (%)', 'Total Points Win (%)', 'Return Points Win (%)', 'Dominant Rate']
for attr in attrs:
    df[attr] = pd.to_numeric(df[attr])

# define simple linear regression function
def slr(y, x):
    model = LinearRegression()
    X = df[x].values.reshape(-1, 1)
    model.fit(X, df[y])

    x_range = np.linspace(X.min(), X.max(), 100)
    y_range = model.predict(x_range.reshape(-1, 1))

    fig = px.scatter(df, x=x, y=y, hover_name='Player', opacity=0.65)
    fig.add_traces(go.Scatter(x=x_range, y=y_range, name="{} = {:.2f} + {:.2f} * {} (R^2 = {:.4f})".format(y, model.intercept_, model.coef_[0], x, model.score(X, df[y]))))

    fig.update_layout(
        title_text = y + ' ~ ' + x,
        xaxis_title = x,
        yaxis_title = y,
        showlegend = True,
        template = 'plotly_dark',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig

# define multiple linear regression function
def mlr(y, x):
    try:
        X = df[x]
        model = LinearRegression()
        model.fit(X, df[y])

        colors = ['Positive' if c > 0 else 'Negative' for c in model.coef_]

        fig = px.bar(
            x=X.columns, y=model.coef_, color=colors,
            color_discrete_sequence=['gold', 'skyblue'],
            labels=dict(x='Feature', y='Linear coefficient'),
            title='R^2 = {:.4f}'.format(model.score(X, df[y])),
        )
    except:
        fig = go.Figure()

    fig.update_layout(
        showlegend = True,
        template = 'plotly_dark',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    return fig

# create app
dash.register_page(__name__, name = 'DSTennis')

layout = html.Div(children=[
    html.Div(children=[
        # section for slr
        html.Div(children=[
            html.Br(),
            html.Div(children=[
                dcc.Dropdown(id="slry", options = attrs,  value = 'Winning Ratio', placeholder = 'Dependent Variable',clearable = False, style = {'background-color': 'rgb(17,17,17)'}),
                dcc.Dropdown(id="slrx", options = attrs, value = 'Dominant Rate', placeholder = 'Independent Variable', clearable = False, style = {'background-color': 'rgb(17,17,17)'}),
            ]
            ),
            dcc.Graph(id='slr', figure = slr('Winning Ratio', 'Dominant Rate')),
        ], className='column2'
        ),
        # section for mlr
        html.Div(children=[
            html.Br(),
            html.Div(children=[
                dcc.Dropdown(id="mlry", options = attrs,  value = 'Winning Ratio', placeholder = 'Dependent Variable',clearable = False, style = {'background-color': 'rgb(17,17,17)'}),
                dcc.Dropdown(id="mlrx", options = attrs, value = ['Ace (%)', '1st Serve In (%)', '2nd Serve Win (%)', 'Return Points Win (%)', 'Double Fault (%)'], placeholder = 'Independent Variable', clearable = False, multi = True,style = {'background-color': 'rgb(17,17,17)'}),
            ]
            ),
            dcc.Graph(id='mlr', figure = mlr('Winning Ratio', ['Ace (%)', '1st Serve In (%)', '2nd Serve Win (%)', 'Return Points Win (%)', 'Double Fault (%)'])),
        ], className='column2'
        ),
    ], style = {'text-align': 'center'}, className='row3'
    ), 
]
)

# slr
@dash.callback(
    Output('slr', 'figure'),
    [Input('slry', 'value')],
    [Input('slrx', 'value')],
)
def update_slr(y, x):
    fig = slr(y, x)
    return fig

# mlr
@dash.callback(
    Output('mlr', 'figure'),
    [Input('mlry', 'value')],
    [Input('mlrx', 'value')],
)
def update_mlr(y, x):
    fig = mlr(y, x)
    return fig
