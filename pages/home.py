import dash
from dash import html

dash.register_page(__name__, path='/', name = 'Home')

layout = html.Div(children=[
    html.H1(children='This is a Tennis Data Hub made by Jerry Cheng.'),
    html.H2(children='Special thanks for Jerry Zhang for useful suggestions.')
])