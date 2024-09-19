from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

'''
Callbacks:

dpto-cconna-dropdown: Departamentos

prov-cconna-dropdown: Provincias

dist-cconna-dropdown: Distritos

tipo-cconna-dropdown: Tipos de CCONNA

creacion-cconna-dropdown: Estado de creación de CCONNA

vigencia-cconna-dropdown: Estado de vigencia de CCONNA



'''

def get_layout():
    layout = html.Div([
        dbc.Container([
            html.H1('Visualizador de Datos de los CCONNA', className='text-center my-4 display-4'),
            
            # Filtros de Búsqueda
            dbc.Card([
                dbc.CardBody([
                    html.H2('Búsqueda por ubigeo', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Departamento:', className='fw-bold'),
                            dcc.Dropdown(id='dpto-cconna-dropdown', className='mb-2'),
                        ], md=3),
                        dbc.Col([
                            html.Label('Provincia:', className='fw-bold'),
                            dcc.Dropdown(id='prov-cconna-dropdown', className='mb-2'),
                        ], md=3),
                        dbc.Col([
                            html.Label('Distrito:', className='fw-bold'),
                            dcc.Dropdown(id='dist-cconna-dropdown', className='mb-2'),
                        ], md=3),
                        dbc.Col([
                            html.Label('Tipo de CCONNA:', className='fw-bold'),
                            dcc.Dropdown(id='tipo-cconna-dropdown', multi=True, className='mb-2'),
                        ], md=3),
                    ], className='mb-3'),

                    html.H2('Búsqueda por estado de CCONNA', className='card-title mb-3'),
                    dbc.Row([
                            dbc.Col([
                                html.Label('Estado de Registro:', className='fw-bold'),
                                dcc.Dropdown(
                                    id='registro-cconna-dropdown',
                                    className='mb-2'
                                ),
                            ], md=4),
                            dbc.Col([
                                html.Label('Estado de Creación:', className='fw-bold'),
                                dcc.Dropdown(
                                    id='creacion-cconna-dropdown',
                                    className='mb-2'
                                ),
                            ], md=4),
                            dbc.Col([
                                html.Label('Estado de Operativa:', className='fw-bold'),
                                dcc.Dropdown(
                                    id='operativa-cconna-dropdown',
                                    className='mb-2'
                                ),
                            ], md=4),
                    ], className='mb-3'),
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Sobre los filtros de estado", className="card-title"),
                            html.P([
                                "Los filtros de estado del CCONNA funcionan de la siguiente manera:",
                                html.Ul([
                                    html.Li("Registro: Indica si el CCONNA está registrado en la base de datos de la DSLD"),
                                    html.Li("Creación: Muestra si el CCONNA ha sido oficialmente creado, lo que implica tener documentos registrados y actualizados."),
                                    html.Li("Operativa: Señala si el CCONNA está actualmente en funcionamiento dentro de las fechas de inicio y fin establecidas.")
                                ]),
                                "Estos filtros son interdependientes: un CCONNA debe estar 'Registrado' para poder estar 'Creado', y debe estar 'Creado' para poder estar 'Operativo'."
                            ])
                        ])
                    ], className="mb-3"),
                    
                    # Gráficos
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='cconna-por-ubicacion'), width=12, className='mb-3'),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='cconna-por-tipo'), md=4, className='mb-3'),
                        dbc.Col(dcc.Graph(id='cconna-por-creacion'), md=4, className='mb-3'),
                        dbc.Col(dcc.Graph(id='cconna-por-operativa'), md=4, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            # Tabla de CCONNA Filtrados
            dbc.Card([
                dbc.CardBody([
                    html.H2('Desglose de CCONNA Filtrados', className='card-title mb-3'),
                    html.Div([
                        dash_table.DataTable(
                            id='tabla-cconna',
                            columns=[
                                {"name": "Ubigeo", "id": "ubigeo"},
                                {"name": "Tipo de CCONNA", "id": "tipo_cconna"},
                                {"name": "Nombre del CCONNA", "id": "nombre_cconna"},
                                {"name": "Especialista Encargado", "id": "estado_creacion"},
                                {"name": "Vigencia", "id": "vigencia"},
                            ],
                            page_current=0,
                            page_size=10,
                            page_action='custom',
                            style_table={'overflowX': 'auto'},
                            style_cell={
                                'height': 'auto',
                                'minWidth': '100px', 'width': '150px', 'maxWidth': '180px',
                                'whiteSpace': 'normal',
                                'textOverflow': 'ellipsis',
                                'overflow': 'hidden'
                            },
                            style_header={
                                'backgroundColor': 'rgb(230, 230, 230)',
                                'fontWeight': 'bold'
                            },
                            style_data_conditional=[
                                {
                                    'if': {'row_index': 'odd'},
                                    'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ],
                            css=[{
                                'selector': '.dash-table-tooltip',
                                'rule': 'background-color: white; font-family: monospace; max-width: 500px !important;'
                            }],
                            tooltip_delay=0,
                            tooltip_duration=None
                        ),
                    ], style={'overflowX': 'auto'}),
                    dbc.Pagination(id='pagination-cconna', max_value=10, fully_expanded=False, className='mt-3'),
                ])
            ], className='mb-4 shadow'),
            
            # Histórico de CCONNA Creados
            dbc.Card([
                dbc.CardBody([
                    html.H2('Histórico de CCONNA Creados', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Fecha de inicio:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-inicio-historico',
                                min_date_allowed=pd.to_datetime('1990-01-01'),
                                max_date_allowed=pd.to_datetime('2030-12-31'),
                                initial_visible_month=pd.to_datetime('2010-01-01'),
                                date=pd.to_datetime('2010-01-01'),
                                className='mb-2'
                            ),
                        ], md=3),
                        dbc.Col([
                            html.Label('Fecha de fin:', className='fw-bold'),
                            dcc.DatePickerSingle(
                                id='fecha-fin-historico',
                                min_date_allowed=pd.to_datetime('1990-01-01'),
                                max_date_allowed=pd.to_datetime('2030-12-31'),
                                initial_visible_month=pd.to_datetime('2024-12-31'),
                                date=pd.to_datetime('2024-12-31'),
                                className='mb-2'
                            ),
                        ], md=3),
                    ], className='mb-3'),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='historico-cconna-creados'), width=12),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            # Búsqueda por Ubigeo
            dbc.Card([
                dbc.CardBody([
                    html.H2('Búsqueda de CCONNA por Ubigeo', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            dbc.InputGroup([
                                dbc.Input(id='ubigeo-input', type='text', placeholder='Ingrese el código Ubigeo del CCONNA'),
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
