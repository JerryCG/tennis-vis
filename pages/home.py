import dash
from dash import html

# create page
dash.register_page(__name__, path='/', name = 'Home')

layout = html.Div(children=[
    html.H1(children='A Tennis Data Hub made by Jerry Cheng'),
    html.Ul(children=[
        html.Li('Special thanks for my best friend Jerry Zhang for suggestions.'),
        html.Li(children=['My GitHub Repository at:',html.A('tennis-vis', href = 'https://github.com/JerryCG/tennis-vis', target="_blank", style = {'font-size': '18px'}), ', where you can see a whole discription of functionality.']),
        html.Li('Let us first see the map of ATP Grand Slam Champions, click and see details!'),
    ], style = {'display': 'inline-block', 'text-align': 'left'}
    ),
    html.Div(children=[
        html.H2('A Network for ATP GS Champions in Tennis History'),
        html.Iframe(
            src='https://flo.uri.sh/visualisation/11884546/embed',
            title='Interactive or visual content',
            className='flourish-embed-iframe',
            style={'width': '90%', 'height':'500px', 'max-width': '800px'}, 
            sandbox='allow-same-origin allow-forms allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox allow-top-navigation-by-user-activation',
        ),
    ])
], style = {'text-align': 'center'}
)