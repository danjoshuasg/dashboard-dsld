from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

def get_layout():
    layout = html.Div([
        dbc.Container([
            html.H1('Visualizador de datos del CCONNA)', className='text-center my-4 display-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Filtros de Búsqueda', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Región:', className='fw-bold'),
                            dcc.Dropdown(id='region-cconna-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Provincia:', className='fw-bold'),
                            dcc.Dropdown(id='provincia-cconna-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Distrito:', className='fw-bold'),
                            dcc.Dropdown(id='distrito-cconna-dropdown', className='mb-2'),
                        ], md=4),
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Tipo de CCONNA:', className='fw-bold'),
                            dcc.Dropdown(id='tipo-cconna-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Estado:', className='fw-bold'),
                            dcc.Dropdown(id='estado-cconna-dropdown', className='mb-2'),
                        ], md=4),
                    ], className='mb-3'),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Resumen de CCONNA', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='cconna-por-region'), md=6, className='mb-3'),
                        dbc.Col(dcc.Graph(id='cconna-por-tipo'), md=6, className='mb-3'),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='cconna-por-estado'), md=6, className='mb-3'),
                        dbc.Col(dcc.Graph(id='cconna-timeline'), md=6, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Detalle de CCONNA', className='card-title mb-3'),
                    dash_table.DataTable(
                        id='tabla-cconna',
                        columns=[
                            {"name": "Registro", "id": "REGISTRO"},
                            {"name": "Región", "id": "Región"},
                            {"name": "Provincia", "id": "Provincia"},
                            {"name": "Distrito", "id": "Distrito"},
                            {"name": "Tipo de CCONNA", "id": "Tipo de CCONNA"},
                            {"name": "Nombre del CCONNA", "id": "Nombre del CCONNA"},
                            {"name": "Fecha de inicio", "id": "Fecha de inicio del CCONNA"},
                            {"name": "Fecha de término", "id": "Fecha de termino del CCONNA"},
                            {"name": "Estado", "id": "ESTADO"},
                        ],
                        page_current=0,
                        page_size=10,
                        page_action='custom',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '100px', 'width': '100px', 'maxWidth': '150px',
                            'whiteSpace': 'normal'
                        },
                    ),
                    dbc.Pagination(id='pagination-cconna', max_value=10, fully_expanded=False, className='mt-3'),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Información Detallada del CCONNA', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id='cconna-input', type='text', placeholder='Ingrese Registro o Nombre del CCONNA'),
                                dbc.Button('Buscar', id='buscar-cconna-btn', color='primary'),
                            ], className='mb-2'),
                        ], md=6),
                    ]),
                    html.Div(id='cconna-error-message', className='text-danger mb-2'),
                    html.Div(id='cconna-results', className='mt-2'),
                ])
            ], className='mb-4 shadow'),
        ], fluid=True)
    ])

    return layout