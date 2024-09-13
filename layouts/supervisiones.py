from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

def get_layout():
    layout = html.Div([
        dbc.Container([
            html.H1('Visualizador de Supervisiones de las DNA', className='text-center my-4 display-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Filtros de Búsqueda', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Departamento:', className='fw-bold'),
                            dcc.Dropdown(id='dpto-supervision-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Provincia:', className='fw-bold'),
                            dcc.Dropdown(id='prov-supervision-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Distrito:', className='fw-bold'),
                            dcc.Dropdown(id='dist-supervision-dropdown', className='mb-2'),
                        ], md=4),   
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Fecha de inicio:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-inicio-supervision',
                                min_date_allowed=pd.to_datetime('2024-01-01'),
                                max_date_allowed=pd.to_datetime('2024-12-31'),
                                initial_visible_month=pd.to_datetime('2024-01-01'),
                                date=pd.to_datetime('2024-01-01'),
                                className='mb-2'
                            ),
                        ], md=3),
                        dbc.Col([
                            html.Label('Fecha de fin:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-fin-supervision',
                                min_date_allowed=pd.to_datetime('2024-01-01'),
                                max_date_allowed=pd.to_datetime('2024-12-31'),
                                initial_visible_month=pd.to_datetime('2024-12-31'),
                                date=pd.to_datetime('2024-12-31'),
                                className='mb-2'
                            ),
                        ], md=3),
                        dbc.Col([
                            html.Label('Supervisor:', className='fw-bold'),
                            dcc.Dropdown(id='supervisor-dropdown', multi=True, className='mb-2'),
                        ], md=3),
                        dbc.Col([
                            html.Label('Tipo de Supervisión:', className='fw-bold'),
                            dcc.Dropdown(id='tipo-supervision-dropdown', multi=True, className='mb-2'),
                        ], md=3),
                    ], className='mb-3'),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Resumen de Supervisiones', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='supervisiones-por-tiempo'), md=6, className='mb-3'),
                        dbc.Col(dcc.Graph(id='supervisiones-por-tipo'), md=6, className='mb-3'),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='supervisiones-por-supervisor'), md=6, className='mb-3'),
                        dbc.Col(dcc.Graph(id='supervisiones-por-ubicacion'), md=6, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Detalle de Supervisiones', className='card-title mb-3'),
                    dash_table.DataTable(
                        id='tabla-supervisiones',
                        columns=[
                            {"name": "Código", "id": "codigo"},
                            {"name": "Código DNA", "id": "codigo_dna"},
                            {"name": "Fecha de Supervisión", "id": "f_supervision"},
                            {"name": "Supervisor", "id": "supervisor"},
                            {"name": "Tipo de Supervisión", "id": "tipo_supervisión"},
                            {"name": "Departamento", "id": "dpto"},
                            {"name": "Provincia", "id": "prov"},
                            {"name": "Distrito", "id": "dist"},
                            {"name": "Resumen", "id": "resumen"},
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
                    dbc.Pagination(id='pagination-supervisiones', max_value=10, fully_expanded=False, className='mt-3'),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Búsqueda de Supervisiones', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id='supervision-input', type='text', placeholder='Ingrese Código DNA o Código de Supervisión'),
                                dbc.Button('Buscar', id='buscar-supervision-btn', color='primary'),
                            ], className='mb-2'),
                        ], md=6),
                    ]),
                    html.Div(id='supervision-error-message', className='text-danger mb-2'),
                    html.Div(id='supervision-results', className='mt-2'),
                ])
            ], className='mb-4 shadow'),
        ], fluid=True)
    ])

    return layout