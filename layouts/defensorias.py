from dash import html, dcc
import dash_bootstrap_components as dbc

def get_layout():
    layout = html.Div([
        html.Div([  # Contenedor principal
            html.H1('Visualizador de datos de Defensorías', className='mb-4'),
                dbc.Row([
                    html.H2('Consolidado por ubigeo', className='mb-3'),
                    # Filtros en cascada
                    dbc.Row([
                        dbc.Col([
                            html.Label('Seleccionar Departamento:'),
                            dcc.Dropdown(id='dpto-dna-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Seleccionar Provincia:'),
                            dcc.Dropdown(id='prov-dna-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Seleccionar Distrito:'),
                            dcc.Dropdown(id='dist-dna-dropdown', className='mb-2'),
                        ], md=4),
                    ], className='mb-4'),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label('Filtrar por Estado de Acreditación:'),
                            dcc.Dropdown(id='estado-dna-dropdown', multi=True, className='mb-4'),
                        ]),
                        dbc.Col([
                            html.Label('Filtrar por Tipo de DNA:'),
                            dcc.Dropdown(id='tipo-dna-dropdown', multi=True, className='mb-4'),
                        ]),
                    ]),
                    # Gráficos 
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='dna-por-ubicacion'),
                        ], width=12),
                    ], className='mb-4'),
                    
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id='dna-por-estado'),
                        ], width=12),
                    ], className='mb-4'),
            ]),
            dbc.Row([
                html.H2('Histórico', className='mb-3')

            ]),

            # Sección de búsqueda por código de DNA
            dbc.Row([
                dbc.Col([
                    html.H2('Búsqueda por Código de DNA', className='mb-3'),
                    dbc.Input(id='dna-input', type='text', placeholder='Ingrese Código de DNA', className='mb-2'),
                    dbc.Button('Buscar', id='buscar-dna-btn', color='primary', className='mb-2'),
                    html.Div(id='dna-error-message', style={'color': 'red'}),
                    html.Div(id='dna-results'),
                ]),
            ]),
        ], style={
            'marginLeft': '250px',  # Ancho del navbar
            'padding': '20px',
            'paddingTop': '40px', 

        }),
    ])
    
    return layout