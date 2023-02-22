# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import html


# create app
dash.register_page(__name__, name = 'GeoTennis')

layout = html.Div(children=[
    # section display a given ATP Ranking Date's Top 100 Players geographic distribution
    html.Div(children=[
        html.H2('ATP Top100 Geographical Distribution from 2000-01-10 to 2023-02-20'),
        html.Iframe(
            src='https://flo.uri.sh/visualisation/11920998/embed',
            title='Interactive or visual content',
            className='flourish-embed-iframe',
            style={'height':'600px', 'width': '60%', 'min-width': '300px'}, 
            sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
        ),
    ], style = {'text-align': 'center'}
    ), 
]
)


