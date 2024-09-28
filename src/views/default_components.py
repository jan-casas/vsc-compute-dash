import dash_bootstrap_components as dbc
from dash import html, dcc

# Header
default_header = dbc.NavbarSimple(
    children=[
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
            dcc.Markdown(
                '''
                
                ### Key Features:
                
                - **Cloud-Based Grasshopper Scripting:** Access Grasshopper from any device with 
                an internet 
                connection. Collaborate 
                seamlessly with colleagues and clients in real-time, no matter where they are.
                
                - **Effortless Data Storage:**`this` seamlessly integrates with Speckle, 
                a leading platform for 
                storing and sharing 
                design and construction data. Your projects and data are securely stored and 
                accessible at all 
                times.
                
                - **Smart Commit Filtering:** Make data-driven decisions with ease.`this` allows 
                you to filter 
                the best commits based 
                on the data it generates. Whether you're optimizing designs, comparing versions, 
                or conducting 
                data analysis, 
                you're in control.
                
                ### Get Started:
                
                If you're ready to unlock the full potential of Grasshopper scripting in the cloud, 
                sign up for`this` today. Discover 
                a world of new possibilities, make data-driven design decisions, and take your 
                architecture, 
                design, and data science 
                projects to the next level.
                            '''
            ),
        ], style={'margin-left': '40px', 'margin-right': '40px', 'margin-bottom': '16px',
                  'margin-top': '20px'})
    ], id='modal', size='lg', scrollable=False, is_open=True,
        style={'width': '100%', 'height': '100%', 'padding': '0px', 'margin': '0px'}),
])
