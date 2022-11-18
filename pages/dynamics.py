import dash
from dash import html

dash.register_page(__name__, name = 'Dynamics')

layout = html.Div(children = [
        html.H2('Dynamic ATP Top10 from 2000 to 2022', style = {'padding-left': '10px'}),
        html.Iframe(
            src='https://flo.uri.sh/visualisation/11862538/embed',
            title='Interactive or visual content',
            className='flourish-embed-iframe',
            style={'width':'50%','height':'500px', 'min-width': '500px', 'margin-left': '10px'}, 
            sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
        ),
        html.Br(),
        html.Br()
    ])

