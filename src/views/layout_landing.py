import sys

import dash
import dash_bootstrap_components as dbc
from dash import dash_table, dcc, html

from src.config.settings import AZURE_CHATBOT
from src.static.style import (CONTENT_STYLE, SIDEBAR_HIDDEN)
from src.utils.utils_speckle import branch_names, initial_branch
from src.views.layout_api_reference import docs_body
from src.views.layout_default import app_header

sys.path.insert(0, '/static/style.py')
sys.path.insert(0, '/apps/utils_plotly.py')

# Register this page
dash.register_page(__name__, path="/", title='VSC - Compute',
                   image_url='/static/assets/icons/hoja.ico')

# Define the app landing layouts
app_layout = dbc.Row([
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
        # dbc.Input(id='input_url_text', type='text',
        #           placeholder='Enter selected commit url', style={'width': '50%'}, size='sm'),

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
        style=SIDEBAR_HIDDEN,
    ),
    dbc.Col(
        dbc.Row([
            html.Iframe(id="compute-iframe",
                        src='http://localhost:3000/examples/docString_panels/',
                        width='100%', height='900px'),
            html.H3(children='Select the Compute Script you want to run'),
            dbc.Col(
                dcc.Dropdown(
                    id='dropdown-compute-manufacturers',
                    options=[{'label': i, 'value': i} for i in
                             ['Corbalán/uglass_facade_tint', 'Garnica/wood_panel_wall',
                              'Garnica/wood_panel_floor',
                              'Garnica/wood_panel_ceiling']],
                    value='Corbalán/uglass_facade_tint',
                    placeholder="Selecciona un fabricante y el sistema constructivo",
                    className='dropUp'
                ),
            ),
            dbc.Col(
                dcc.Dropdown(
                    id='dropdown-compute-commit',
                    options=[{'label': i, 'value': i} for i in branch_names],
                    value=branch_names[3],
                    placeholder="Selecciona un commit sobre el que realizar el procesamiento",
                    className='dropUp'
                ),
            ),
        ])
    ),
    dbc.Col(
        dbc.Row([
            html.Iframe(id="speckle-iframe",
                        src='https://speckle.xyz/embed?stream=0e5d383e76&commit=570241446f'
                            '&transparent=true&autoload'
                            '=true&hidesidebar=true&hidecontrols=true',
                        width='100%', height='900px'),
            html.H3(children='Select the branches you want to visualize'),
            dcc.Dropdown(id='dropdown_branches',
                         options=[{'label': i, 'value': i} for i in branch_names],
                         value=[initial_branch],
                         multi=True,
                         className='dropUp'
                         ),
            dcc.Markdown('''
            *https://www.nomad.as/html%20css/durango2_14.php*
            '''),
        ])
    )
], style={'width': 'calc(100% - 12rem)', 'margin-left': '6rem', 'margin-right': '6rem'})

collapsable_parameter = html.Div(
    dbc.Collapse(
        dbc.Card(
            dbc.CardBody([
                dbc.Row([
                    dbc.Col(
                        html.Label('Distance Panels:'),
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
                        html.Label('Radius Distance:'),
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
                        html.Label('Span in between:'),
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
                        style={'justify-content': 'center', 'font-color': 'white', 'margin': '10px'}
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
            ])
        ),
        id="collapse",
        style={'width': '50%', 'align-items': 'center', 'margin-top': '60px',
               'justify-content': 'center'}
    ), className='collapse-container'
)

modal_text = '''

### Key Features:

- **Cloud-Based Grasshopper Scripting:** Access Grasshopper from any device with an internet 
connection. Collaborate 
seamlessly with colleagues and clients in real-time, no matter where they are.

- **Effortless Data Storage:**`this` seamlessly integrates with Speckle, a leading platform for 
storing and sharing 
design and construction data. Your projects and data are securely stored and accessible at all 
times.

- **Smart Commit Filtering:** Make data-driven decisions with ease.`this` allows you to filter 
the best commits based 
on the data it generates. Whether you're optimizing designs, comparing versions, or conducting 
data analysis, 
you're in control.

### Get Started:

If you're ready to unlock the full potential of Grasshopper scripting in the cloud, 
sign up for`this` today. Discover 
a world of new possibilities, make data-driven design decisions, and take your architecture, 
design, and data science 
projects to the next level.
            '''
app_modal = html.Div([
    dbc.Modal([
        dbc.ModalHeader(
            html.Div([
                html.Div([
                    html.H3(id='modal-title',
                            children='Grasshopper Scripting in the Cloud'),
                    dcc.Markdown('''`this` is a cutting-edge application that brings the power of 
                    Grasshopper 
                    scripting to the cloud, enabling you to design, analyze, and collaborate like 
                    never before. As an 
                    architect, designer, data scientist, or programmer with a thirst for 
                    knowledge and discovery, 
                    this tool is tailored to your needs.
''')], id='grid-item-1', className='grid-item'),
            ], style={'display': 'flex', 'alignItems': 'center', 'margin-left': '40px',
                      'margin-right': '40px',
                      'margin-top': '40px', 'margin-bottom': '15px'})
        ),
        # Responsive information
        dbc.ModalBody(id='default-modal', children=[
            dcc.Markdown(modal_text),
        ], style={'margin-left': '40px', 'margin-right': '40px', 'margin-bottom': '16px',
                  'margin-top': '20px'})
    ], id='modal', size='lg', scrollable=False, is_open=True,
        style={'width': '100%', 'height': '100%', 'padding': '0px', 'margin': '0px'}),
])

toast = html.Div(
    dbc.Toast(
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

chat_modal = html.Div([
    dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div([
                    html.Div([
                        html.H3(id='modal-title',
                                children='Ask me anything! AEC Bot at your service'),
                        dcc.Markdown('''`this` is a cutting-edge application that brings the 
                        power of Grasshopper 
                        scripting to the cloud, enabling you to design, analyze, and collaborate 
                        like never before.
''')], id='grid-item-1', className='grid-item'),
                ], style={'display': 'flex', 'alignItems': 'center', 'margin-left': '40px',
                          'margin-right': '40px',
                          'margin-top': '40px', 'margin-bottom': '15px'})
            ),
            dbc.ModalBody(children=[
                html.Iframe(
                    src=f'https://europe.webchat.botframework.com/embed/test_bot_aec?s='
                        f'{AZURE_CHATBOT}',
                    style={"height": "600px", "width": "100%"})
            ]),
        ],
        id="modal",
        size="lg",
    )
])

help_modal = html.Div([
    dbc.Modal(
        [
            dbc.ModalHeader(
                html.Div([
                    html.Div([
                        html.H3(id='modal-title',
                                children='Version Control for AEC using Speckle'),
                        dcc.Markdown('''`this` is a cutting-edge application that brings the 
                        power of Grasshopper 
                        scripting to the cloud, enabling you to design, analyze, and collaborate 
                        like never before.
''')], id='grid-item-1', className='grid-item'),
                ], style={'display': 'flex', 'alignItems': 'center', 'margin-left': '40px',
                          'margin-right': '40px',
                          'margin-top': '40px', 'margin-bottom': '15px'})
            ),
            dbc.ModalBody(children=[
                # html.Iframe(src=f'https://europe.webchat.botframework.com/embed/test_bot_aec?s
                # ={AZURE_CHATBOT}',
                # style={"height": "30%", "width": "100%"}),
                docs_body]),
        ],
        id="help_modal",
        size="lg",
    )
])

content = html.Div(
    id="page-content",
    style=CONTENT_STYLE)

storage_layout = html.Div([
    dcc.Store(id='side_click'),
    dcc.Store(id='slider-values-store', storage_type='memory'),
    dcc.Store(id='store-branches-attributes', storage_type='memory'),
    dcc.Store(id='store-branches', storage_type='memory'),
    html.Div(id='dummy-output', style={'display': 'none'}),
])

layout = dbc.Col([
    app_modal,
    storage_layout,
    dbc.Row(app_header),
    dbc.Row(collapsable_parameter),
    dbc.Row(app_layout, style={'margin-top': '60px'}),
    content,
    toast,
    chat_modal,
    help_modal,
])
