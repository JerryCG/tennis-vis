# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html

# create page
dash.register_page(__name__, name = 'Leaderboard')

layout = html.Div(children=[
    # section to displace total titles, wr leaderboard
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H2('ATP Top10 Total Titles (GS + ATP1000 + ATP Finale + Olympics)'),
                html.Iframe(
                    src='https://flo.uri.sh/visualisation/11930272/embed',
                    title='Interactive or visual content',
                    className='flourish-embed-iframe',
                    style={'height':'500px', 'width': '80%'},
                    sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
                ),
            ], className='column2'
            ),
            html.Div(children=[
                html.H2('ATP Top10 Winning Ratio'),
                html.Iframe(
                    src='https://flo.uri.sh/visualisation/11931399/embed',
                    title='Interactive or visual content',
                    className='flourish-embed-iframe',
                    style={'height':'500px', 'width': '80%'},
                    sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
                ), 
            ], className='column2'
            ),
        ], className = 'row2'
        ),
    ],
    ),
    # section to displace gs, atp1000+finale leaderboard
    html.Div(children=[
        html.Div(children=[
            html.Div(children=[
                html.H2('ATP Top10 Grand Slams'),
                html.Iframe(
                    src='https://flo.uri.sh/visualisation/11931551/embed',
                    title='Interactive or visual content',
                    className='flourish-embed-iframe',
                    style={'height':'500px', 'width': '80%'},
                    sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
                ),
            ], className='column2'
            ),
            html.Div(children=[
                html.H2('ATP Top10 ATP1000 + ATP Finale'),
                html.Iframe(
                    src='https://flo.uri.sh/visualisation/11931597/embed',
                    title='Interactive or visual content',
                    className='flourish-embed-iframe',
                    style={'height':'500px', 'width': '80%'},
                    sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
                ), 
            ], className='column2'
            ),
        ], className = 'row2'
        ),
    ],
    ), 
], style = {'text-align': 'center'}
)