from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

def get_layout():
    layout = html.Div([
        dbc.Container([
            html.H1('Visualizador de Datos de los Defensores de las DNA', className='text-center my-4 display-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Filtros de Búsqueda', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Departamento:', className='fw-bold'),
                            dcc.Dropdown(id='dpto-defensores-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Provincia:', className='fw-bold'),
                            dcc.Dropdown(id='prov-defensores-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Distrito:', className='fw-bold'),
                            dcc.Dropdown(id='dist-defensores-dropdown', className='mb-2'),
                        ], md=4),   
                    ], className='mb-3'),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label('Cargo de defensor:', className='fw-bold'),
                            dcc.Dropdown(id='cargo-defensores-dropdown', multi=True, className='mb-2'),
                        ], md=6),
                        dbc.Col([
                            html.Label('Ocupación de defensor:', className='fw-bold'),
                            dcc.Dropdown(id='ocupacion-defensores-dropdown', multi=True, className='mb-2'),
                        ], md=6),
                    ], className='mb-3'),
                    
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='defensores-por-ubicacion'), width=12, className='mb-3'),
                    ]),
                    
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='defensores-por-cargo'), md=6, className='mb-3'),
                        dbc.Col(dcc.Graph(id='defensores-por-ocupacion'), md=6, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Resultados de Defensores', className='card-title mb-3'),
                    dash_table.DataTable(
                        id='tabla-defensores',
                        columns=[
                            {"name": "Código DNA", "id": "codigo_dna"},
                            {"name": "Nombres", "id": "nombres"},
                            {"name": "Apellido", "id": "apellido"},
                            {"name": "Cargo", "id": "cargo"},
                            {"name": "DNI", "id": "dni"},
                            {"name": "Ocupación", "id": "ocupacion"},
                        ],
                        page_current=0,
                        page_size=10,
                        page_action='custom',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
                            'whiteSpace': 'normal'
                        },
                    ),
                    dbc.Pagination(id='pagination-defensores', max_value=10, fully_expanded=False, className='mt-3'),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Evolución Histórica de Nombramientos', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Fecha de inicio:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-inicio',
                                min_date_allowed=pd.to_datetime('1995-01-01'),
                                max_date_allowed=pd.to_datetime('2030-12-31'),
                                initial_visible_month=pd.to_datetime('2018-11-01'),
                                date=pd.to_datetime('2018-10-01'),
                                className='mb-2'
                            ),
                        ], md=3),
                        dbc.Col([
                            html.Label('Fecha de fin:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-fin',
                                min_date_allowed=pd.to_datetime('1995-01-01'),
                                max_date_allowed=pd.to_datetime('2030-12-31'),
                                initial_visible_month=pd.to_datetime('2024-12-31'),
                                date=pd.to_datetime('2024-12-12'),
                                className='mb-2'
                            ),
                        ], md=3),
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='nombramientos-por-fechas'), width=12),
                    ]),
                ])
            ], className='mb-4 shadow'),

            dbc.Card([
                dbc.CardBody([
                    html.H2('Búsqueda de Defensores', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id='defensor-input', type='text', placeholder='Ingrese Nombre, Apellido o DNI del Defensor'),
                                dbc.Button('Buscar', id='buscar-defensor-btn', color='primary'),
                            ], className='mb-2'),
                        ], md=6),
                    ]),
                    html.Div(id='defensor-error-message', className='text-danger mb-2'),
                    html.Div(id='defensor-results', className='mt-2'),
                ])
            ], className='mb-4 shadow'),
        ], fluid=True)
    ])

    return layout