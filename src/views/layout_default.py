import dash_bootstrap_components as dbc
from dash import html

# HEADER
app_header = dbc.NavbarSimple(
    children=[
        dbc.Button("Why this?", id="open_help_button", color="link", className="mr-1", n_clicks=0, outline=True),
        dbc.Button("Speckle OP", id="speckle_data_sidebar", color="link", className="mr-1", n_clicks=0, outline=True,
                   style={"margin-right": "10px"}),
        dbc.Button('Compute!', id='update_speckle_iframe', n_clicks=0,
                   color='primary'),
    ],
    sticky="top",
    className='app-header'
)

# FOOTER
app_footer = html.Footer([
    html.Div(id='grid-container_sub3', children=[
        html.Div([
            html.Div([
                html.Img(src='/static/icons/life-preserver.svg',
                         className='icon-item-icon',
                         style={'height': '20px', 'width': '20px', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.H3('Help Center'),
                html.P(
                    'Answers to frequently asked account and billing questions.')
            ], style={'marginLeft': '20px', 'textAlign': 'center'})
        ], id='grid-item-51', className='grid-item',
            style={'display': 'flex', 'alignItems': 'center', 'margin': '0px'}),
        html.Div([
            html.Div([
                html.Img(src='/static/icons/search.svg',
                         className='icon-item-icon',
                         style={'height': '20px', 'width': '20px', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.H3('Disclosure'),
                html.P(
                    'Ask questions and discuss topics with other developers.')
            ], style={'marginLeft': '20px', 'textAlign': 'center'})
        ], id='grid-item-52', className='grid-item',
            style={'display': 'flex', 'alignItems': 'center', 'margin': '0px'}),
        html.Div([
            html.Div([
                html.Img(src='/static/icons/broadcast.svg',
                         className='icon-item-icon',
                         style={'height': '20px', 'width': '20px', 'alignItems': 'center', 'justifyContent': 'center'}),
                html.H3('Service Status'),
                html.P(
                    'Check the status of the API services.')
            ], style={'marginLeft': '20px', 'textAlign': 'center'})
        ], id='grid-item-53', className='grid-item',
            style={'display': 'flex', 'alignItems': 'center', 'margin': '0px'}),
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'grid-gap': '44px', 'marginTop': '24px',
              'width': '45%', 'margin-left': 'auto', 'margin-right': 'auto'}),
], style={'width': '100%', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-top': '50px',
          'background-color': '#f7f7f8', 'height': '200px'})
