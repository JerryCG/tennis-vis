# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash

# create app
app = Dash(__name__, use_pages=True, meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ])

# set server
server = app.server

# set app title
app.title = "TennisVis"

# design app layout
app.layout = html.Div([
    # section for head
    html.Div(children=[
        html.Img(src='assets/logotennis.png', alt='logo', style={'width': '180px', 'margin-left': '-20px'}),
        html.Div(children=[
            html.Div(children=[
                html.Div(
                    "TennisVis", style = {'color': 'gold', 'font-size': '100px', 'margin-top': '-30px', 'margin-right': '-10px', 'display': 'inline-block'}
                ),
                # html.Div(children=[
                #     html.Img(src='assets/2023logonew.png', alt='2023', style={'width': '850px', 'height':'150px', 'margin-left': '-610px', 'margin-top':'-30px'}),
                # ], style = {'display': 'inline-block', 'z-index': '-1', 'position': 'absolute'},
                # ),
            ]
            ),
            html.Div(
                "Last Update: 2025-04-07", style = {'font-size': '20px', 'font-style': 'italic'}
            ),
        ], style = {'text-align': 'center'}
    ),
    ]),
    # section for navigation bar
    html.Div(
        [
            html.Span(
                dcc.Link(
                     f"{page['name']}", href=page["relative_path"], 
                ), className='column6'
            )
            for page in dash.page_registry.values()
        ], id = 'menu', className = 'row6'
    ),

	dash.page_container,

    # section for footer
    html.Footer(
        children=[
            html.Div('2025 Copyright of raw data belong to tennisabstract.com, atptour.com - fair use for scraping, processing, and visualizing tennis data'),
            html.Div('This is TennisVis Version 2.4 made with heart for tennis lovers. For any suggestions or comments, please email me at chengguo@uchicago.edu')
        ]
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)