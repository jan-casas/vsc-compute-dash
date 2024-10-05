import dash_bootstrap_components as dbc
from dash import html

from static.static_docs import readme_body, readme_header

# Header
default_header = dbc.NavbarSimple(
    children=[
        dbc.Button("Parts", id="speckle-data-count", color="link",
                   className="mr-1 header-button",
                   n_clicks=0, outline=True,
                   style={"margin-right": "10px"}),
        dbc.Button("Speckle OP", id="speckle-data-sidebar", color="link",
                   className="mr-1 header-button",
                   n_clicks=0, outline=True,
                   style={"margin-right": "10px"}),
        dbc.Button('Compute!', id='update-speckle-iframe', n_clicks=0,
                   className='header-button',
                   color='primary'),
    ],
    sticky="top",
    className='app-header',
    style={'justifyContent': 'flex-start'}
)

# Footer
default_footer = html.Footer([
    html.Div(id='grid-container_sub3', children=[
        html.Div([
            html.Div([
                html.Img(src='/static/icons/life-preserver.svg',
                         className='icon-item-icon',
                         style={'height': '20px', 'width': '20px', 'alignItems': 'center',
                                'justifyContent': 'center'}),
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
                         style={'height': '20px', 'width': '20px', 'alignItems': 'center',
                                'justifyContent': 'center'}),
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
                         style={'height': '20px', 'width': '20px', 'alignItems': 'center',
                                'justifyContent': 'center'}),
                html.H3('Service Status'),
                html.P(
                    'Check the status of the API services.')
            ], style={'marginLeft': '20px', 'textAlign': 'center'})
        ], id='grid-item-53', className='grid-item',
            style={'display': 'flex', 'alignItems': 'center', 'margin': '0px'}),
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(3, 1fr)', 'grid-gap': '44px',
              'marginTop': '24px',
              'width': '45%', 'margin-left': 'auto', 'margin-right': 'auto'}),
], style={'width': '100%', 'margin-left': 'auto', 'margin-right': 'auto', 'margin-top': '50px',
          'background-color': '#f7f7f8', 'height': '200px'})

# Modals and Toasts
default_toast = html.Div(dbc.Toast(
    children="La petición se ha realizado correctamente, en breve aparecerá actualizado el "
             "modelo.",
    id="positioned-toast",
    header="Recibido! 🤯",
    is_open=False,
    dismissable=True,
    # icon="success",
    # top: 66 positions the toast below the navbar
    style={"position": "fixed", "top": 66,
           "right": 10, "width": 350, "zIndex": 9999},
    # color="info",
    duration=5000,
),
)

default_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(
            html.Div([
                html.Div([
                    readme_header
                ], id='grid-item-1', className='grid-item'),
            ], style={'display': 'flex', 'alignItems': 'center', 'margin-left': '40px',
                      'margin-right': '40px',
                      'margin-top': '40px', 'margin-bottom': '15px'})
        ),
        # Responsive information
        dbc.ModalBody(id='default-modal', children=[
            readme_body
        ], style={'margin-left': '40px', 'margin-right': '40px', 'margin-bottom': '16px',
                  'margin-top': '20px'})
    ], id='modal', size='lg', scrollable=True, is_open=True,
        style={'width': '100%', 'height': '100%', 'padding': '0px', 'margin': '0px'}),
])
