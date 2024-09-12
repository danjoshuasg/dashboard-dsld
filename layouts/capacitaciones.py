from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.data_loader import load_capacitaciones_data, load_defensorias_data

def get_layout():
    layout = html.Div([
        html.Div([  # Contenedor principal
            html.H1('Dashboard de Capacitaciones', className='mb-4'),
            
            # Filtros en cascada
            dbc.Row([
                dbc.Col([
                    html.Label('Seleccionar Departamento:'),
                    dcc.Dropdown(id='dpto-capacitaciones-dropdown', className='mb-2'),
                ], md=4),
                dbc.Col([
                    html.Label('Seleccionar Provincia:'),
                    dcc.Dropdown(id='prov-capacitaciones-dropdown', className='mb-2'),
                ], md=4),
                dbc.Col([
                    html.Label('Seleccionar Distrito:'),
                    dcc.Dropdown(id='dist-capacitaciones-dropdown', className='mb-2'),
                ], md=4),
            ], className='mb-4'),
            
            dbc.Row([
                dbc.Col([
                    html.Label('Filtrar por Curso:'),
                    dcc.Dropdown(id='curso-capacitaciones-dropdown', multi=True, className='mb-4'),
                ]),
            ]),
            
            # Gráficos en filas separadas
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='capacitaciones-por-ubicacion'),
                ], width=12),
            ], className='mb-4'),
            
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='capacitaciones-por-curso'),
                ], width=12),
            ], className='mb-4'),
            
            # Sección de búsqueda por DNI
            dbc.Row([
                dbc.Col([
                    html.H2('Búsqueda por DNI', className='mb-3'),
                    dbc.Input(id='dni-input', type='text', placeholder='Ingrese DNI (8 dígitos)', className='mb-2'),
                    dbc.Button('Buscar', id='buscar-btn', color='primary', className='mb-2'),
                    html.Div(id='dni-error-message', style={'color': 'red'}),
                    html.Div(id='dni-results'),
                ]),
            ]),
        ], style={
            'marginLeft': '250px',  # Ancho del navbar
            'padding': '20px',
            'paddingTop': '40px',  # Espacio adicional en la parte superior
        }),
    ])
    
    return layout