import sys

import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from src.static.style import (content_style_dict, sidebar_hidden_dict)
from src.utils.utils_speckle import branch_names, initial_branch
from src.views.default_components import default_header, default_toast, default_modal

sys.path.insert(0, '/static/style.py')
sys.path.insert(0, '/utils/utils_plotly.py')

# Register this page
dash.register_page(__name__, path="/", title='VSC - Compute',
                   image_url='/static/assets/icons/hoja.ico')

# Define the app landing layouts
compute_speckle_layout = dbc.Row([
    dbc.Col([
        dcc.Markdown('''
            ### Speckle Optimal Commit

            This is a plot of the attributes of the objects in the stream. The plot is 
            interactive, so you can select 
            the attributes you want to see. You can also select the objects you want to see by 
            clicking on the legend.

            Each time you filter the data, the plot will update and the table will show the data 
            that is currently 
            being displayed. This will give you the most likely commit that you want to use.        
        ''', style={'margin-top': '20px', 'font-size': '15px', 'font-family': 'Arial'}),
        dcc.Dropdown(
            id='dropdown_commit',
        ),
        dcc.Graph(
            id='speckle_parallel_data',
            figure={}
        ),
        dash_table.DataTable(
            id='table_data',
            columns=[{"name": i, "id": i}
                     for i in ['authorName', 'commitId', 'message']],
            style_cell={
                'fontFamily': 'Arial',
                'fontSize': 14
            },
            page_action='native',
            page_size=5,
        )
    ],
        id="sidebar_data",
        style=sidebar_hidden_dict,
    ),
    dbc.Col(
        dbc.Row([
            html.Span(children='Select the Compute Script you want to run'),
            dbc.Col(
                dcc.Dropdown(
                    id='dropdown-compute-manufacturers',
                    options=[{'label': i, 'value': i} for i in
                             ['Corbalán/uglass_facade_tint', 'Garnica/wood_panel_wall',
                              'Garnica/wood_panel_floor',
                              'Garnica/wood_panel_ceiling']],
                    value='Corbalán/uglass_facade_tint',
                    placeholder="Selecciona un fabricante y el sistema constructivo",
                    # className='dropUp'
                ),
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='dropdown-compute-commit',
                    options=[{'label': i, 'value': i} for i in branch_names],
                    value=branch_names[3],
                    placeholder="Selecciona un commit sobre el que realizar el procesamiento",
                    # className='dropUp'
                ),
            ),
            html.Iframe(id="compute-iframe",
                        src='http://localhost:3000/examples/docString_panels/',
                        width='100%', height='800px'),

        ])
    ),
    dbc.Col(
        dbc.Row([
            html.Span(children='Select the branches you want to visualize'),
            dcc.Dropdown(id='dropdown_branches',
                         options=[{'label': i, 'value': i} for i in branch_names],
                         value=[initial_branch],
                         multi=True,
                         # className='dropUp'
                         ),
            html.Iframe(id="speckle-iframe",
                        src='https://app.speckle.systems/projects/013613abb4/models/cd91d7878f'
                            '&transparent=true&autoload'
                            '=true&hidesidebar=true&hidecontrols=true',
                        width='100%', height='800px'),

        ])
    )
],
    style={'width': 'calc(100% - 12rem)', 'margin-left': '6rem', 'margin-right': '6rem'})

compute_parameters = dbc.Row(
    html.Div(
        dbc.Collapse(
            dbc.Card(
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([

                            dbc.Row([
                                dbc.Col(
                                    html.Span('Distance Panels:'),
                                    width=2
                                ),
                                dbc.Col(
                                    dcc.Slider(
                                        id='compute-count-slider',
                                        min=0,
                                        max=20,
                                        step=1,
                                        value=10,
                                        marks={i: f'{i}' for i in range(0, 21, 2)},
                                    ),
                                ),
                            ]),
                            dbc.Row([
                                dbc.Col(
                                    html.Span('Radius Distance:'),
                                    width=2
                                ),
                                dbc.Col(
                                    dcc.Slider(
                                        id='compute-radius-slider',
                                        min=0,
                                        max=20,
                                        step=1,
                                        value=3,
                                        marks={i: f'{i}' for i in range(0, 21, 2)},
                                    ),
                                ),
                            ]),
                            dbc.Row([
                                dbc.Col(
                                    html.Span('Span in between:'),
                                    width=2
                                ),
                                dbc.Col(
                                    dcc.Slider(
                                        id='compute-span-slider',
                                        min=0,
                                        max=20,
                                        step=1,
                                        value=3,
                                        marks={i: f'{i}' for i in range(0, 21, 2)},
                                    ),
                                ),
                            ]),
                        ]),
                        dbc.Col([
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='dropdown-compute-data',
                                        options=[{'label': i, 'value': i} for i in branch_names],
                                        value=branch_names[3],
                                        placeholder="Selecciona un commit sobre el que realizar el "
                                                    "procesamiento"),
                                    # width=6,
                                    style={'margin': '10px'}
                                ),
                                dbc.Col(
                                    dbc.Button('Bake it in Speckle! 🧑‍🍳🥖', id='bake-button',
                                               className="mr-1",
                                               color='warning',
                                               style={'width': '100%'}),
                                    width=4,
                                    style={'justify-content': 'center', 'font-color': 'white',
                                           'margin': '10px'}
                                )
                            ]),
                            dbc.Row(
                                dbc.Col(
                                    dbc.Input(id='input_commit_message',
                                              type='text',
                                              placeholder='Enter selected commit url',
                                              style={'width': '100%'}),
                                    # width=6,
                                    style={'margin': '10px'}
                                ),
                            ),
                        ]),
                    ]),
                ])
            ),
            id="collapse",
            style={'width': '100%', 'align-items': 'center', 'margin-top': '60px',
                   'justify-content': 'center'},
        )
        , className='collapse-container'
    )
)

content = html.Div(
    id="page-content",
    style=content_style_dict)

metadata_storage = html.Div([
    dcc.Store(id='side_click'),
    dcc.Store(id='slider-values-store', storage_type='memory'),
    dcc.Store(id='store-branches-attributes', storage_type='memory'),
    dcc.Store(id='store-branches', storage_type='memory'),
    html.Div(id='dummy-output', style={'display': 'none'}),
])

layout = dbc.Col([
    default_modal,
    metadata_storage,
    default_header,
    compute_parameters,
    dbc.Row(compute_speckle_layout, style={'margin-top': '60px'}),
    content,
    # default_toast,
])
