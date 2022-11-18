import dash
from dash import html

dash.register_page(__name__, path='/', name = 'Home')

layout = html.Div(children=[
    html.H1(children='A Tennis Data Hub made by Jerry Cheng'),
    html.Ul(children=[
        html.Li('Special thanks for my best friend Jerry Zhang for suggestions.'),
        html.Li(children=['My GitHub Repository at:',html.A('tennis-vis', href = 'https://github.com/JerryCG/tennis-vis', target="_blank", style = {'font-size': '18px'})]),
    ]),
])