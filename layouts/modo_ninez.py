from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

def get_layout():
    layout = html.Div([
        dbc.Container([
            html.H1('Visualizador de Datos de Capacitaciones', className='text-center my-4 display-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Filtros de Búsqueda', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Departamento:', className='fw-bold'),
                            dcc.Dropdown(id='dpto-capacitaciones-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Provincia:', className='fw-bold'),
                            dcc.Dropdown(id='prov-capacitaciones-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Distrito:', className='fw-bold'),
                            dcc.Dropdown(id='dist-capacitaciones-dropdown', className='mb-2'),
                        ], md=4),   
                    ], className='mb-3'),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label('Curso:', className='fw-bold'),
                            dcc.Dropdown(id='curso-capacitaciones-dropdown', multi=True, className='mb-2'),
                        ], md=12),
                    ], className='mb-3'),
                    
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='capacitaciones-por-ubicacion'), width=12, className='mb-3'),
                    ]),
                    
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='capacitaciones-por-curso'), width=12, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Resultados de Capacitaciones', className='card-title mb-3'),
                    dash_table.DataTable(
                        id='tabla-capacitaciones',
                        columns=[
                            {"name": "Curso", "id": "curso"},
                            {"name": "Fecha", "id": "fecha"},
                            {"name": "Departamento", "id": "departamento"},
                            {"name": "Provincia", "id": "provincia"},
                            {"name": "Distrito", "id": "distrito"},
                            {"name": "Participantes", "id": "participantes"},
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
                    dbc.Pagination(id='pagination-capacitaciones', max_value=10, fully_expanded=False, className='mt-3'),
                ])
            ], className='mb-4 shadow'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Evolución Histórica de Capacitaciones', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Fecha de inicio:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-inicio',
                                min_date_allowed=pd.to_datetime('2000-01-01'),
                                max_date_allowed=pd.to_datetime('2030-12-31'),
                                initial_visible_month=pd.to_datetime('2023-01-01'),
                                date=pd.to_datetime('2023-01-01'),
                                className='mb-2'
                            ),
                        ], md=3),
                        dbc.Col([
                            html.Label('Fecha de fin:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-fin',
                                min_date_allowed=pd.to_datetime('2000-01-01'),
                                max_date_allowed=pd.to_datetime('2030-12-31'),
                                initial_visible_month=pd.to_datetime('2024-12-31'),
                                date=pd.to_datetime('2024-12-31'),
                                className='mb-2'
                            ),
                        ], md=3),
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='capacitaciones-por-fechas'), width=12),
                    ]),
                ])
            ], className='mb-4 shadow'),

            dbc.Card([
                dbc.CardBody([
                    html.H2('Búsqueda por DNI', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id='dni-input', type='text', placeholder='Ingrese DNI (8 dígitos)'),
                                dbc.Button('Buscar', id='buscar-btn', color='primary'),
                            ], className='mb-2'),
                        ], md=6),
                    ]),
                    html.Div(id='dni-error-message', className='text-danger mb-2'),
                    html.Div(id='dni-results', className='mt-2'),
                ])
            ], className='mb-4 shadow'),
        ], fluid=True)
    ])

    return layout