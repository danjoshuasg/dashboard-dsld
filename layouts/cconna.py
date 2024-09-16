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
                    html.H2('Filtros de Búsqueda', className='card-title mb-3'),
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
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label('Estado de Creación:', className='fw-bold'),
                            dcc.Dropdown(
                                id='creacion-cconna-dropdown',
                                multi=True,
                                className='mb-2'
                            ),
                        ], md=6),
                        dbc.Col([
                            html.Label('Vigencia del CCONNA:', className='fw-bold'),
                            dcc.Dropdown(
                                id='vigencia-cconna-dropdown',
                                multi=True,
                                className='mb-2'
                            ),
                        ], md=6),
                    ], className='mb-3'),
                    
                    # Gráficos
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='histograma-cconna'), width=12, className='mb-3'),
                    ]),
                    dbc.Row([
                        dbc.Col(dcc.Graph(id='pie-cconna-tipo'), md=4, className='mb-3'),
                        dbc.Col(dcc.Graph(id='pie-cconna-creacion'), md=4, className='mb-3'),
                        dbc.Col(dcc.Graph(id='pie-cconna-vigencia'), md=4, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
            
            # Tabla de CCONNA Filtrados
            dbc.Card([
                dbc.CardBody([
                    html.H2('Desglose de CCONNA Filtrados', className='card-title mb-3'),
                    dash_table.DataTable(
                        id='tabla-cconna',
                        columns=[
                            {"name": "N° REGISTRO", "id": "registro"},
                            {"name": "Ubigeo", "id": "ubigeo"},
                            {"name": "Región", "id": "region"},
                            {"name": "Provincia", "id": "provincia"},
                            {"name": "Distrito", "id": "distrito"},
                            {"name": "Tipo de CCONNA", "id": "tipo_cconna"},
                            {"name": "Nombre del CCONNA", "id": "nombre_cconna"},
                            {"name": "Estado de Creación", "id": "estado_creacion"},
                            {"name": "Vigencia", "id": "vigencia"},
                        ],
                        page_current=0,
                        page_size=10,
                        page_action='custom',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'height': 'auto',
                            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
                            'whiteSpace': 'normal'
                        },
                    ),
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
