import dash
from dash import html

dash.register_page(__name__, name = 'Dynamics')

layout = html.Div(children = [
        html.H2('Dynamic ATP Rankings from 1990 to 2022', style = {'padding-left': '10px'}),
        html.Iframe(
            src = "https://www.youtube.com/embed/jgZSumjsKzg?controls=1&rel=0&playsinline=0&modestbranding=0&autoplay=0&enablejsapi=1&origin=https%3A%2F%2Fstatisticsanddata.org&widgetid=1",
            style = {'width': '70%', 'height': '500px', 'margin-left': '10px'}
        ),
    ])