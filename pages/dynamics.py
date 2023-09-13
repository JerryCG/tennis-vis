import dash
from dash import html

dash.register_page(__name__, name = 'Dynamics')

layout = html.Div(children = [
    html.Div(children=[
        html.Div(children=[
            html.H2('Dynamic ATP Top10 from 2000-01-10 to 2023-09-11'),
            html.Iframe(
                src='https://flo.uri.sh/visualisation/11862538/embed',
                title='Interactive or visual content',
                className='flourish-embed-iframe',
                style={'height':'500px', 'width': '90%'}, 
                sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
            ),
        ],className='column2'
        ), 
        html.Div(children=[
            html.H2('GS Counts of Big ATP Players from 1990 to 2023'),
            html.Iframe(
                src='https://flo.uri.sh/visualisation/11883754/embed',
                title='Interactive or visual content',
                className='flourish-embed-iframe',
                style={'width': '90%', 'height':'500px'}, 
                sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
            ),
        ],className='column2'
        ),
    ], className='row2', style = {'text-align': 'center'}
    ),
    html.Br(),
    html.Br(),
])

