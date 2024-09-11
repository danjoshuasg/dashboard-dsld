from dash import html, dcc
import dash_bootstrap_components as dbc
from utils.data_loader import load_capacitaciones_data, load_defensorias_data

def get_layout():
    # Cargar datos para las opciones de los dropdowns

    layout = dbc.Container([
        html.Div([
            html.H1('Dashboard de Capacitaciones'),
            
            # Filtros en cascada
            html.Div([
                html.Label('Seleccionar Departamento:'),
                dcc.Dropdown(id='dpto-capacitaciones-dropdown'),
                html.Label('Seleccionar Provincia:'),
                dcc.Dropdown(id='prov-capacitaciones-dropdown'),
                html.Label('Seleccionar Distrito:'),
                dcc.Dropdown(id='dist-capacitaciones-dropdown'),
            ]),
            
            html.Div([
                html.Label('Filtrar por Curso:'),
                dcc.Dropdown(id='curso-capacitaciones-dropdown', multi=True)
            ]),
            
            # Gráficos
            dcc.Graph(id='capacitaciones-por-ubicacion'),
            dcc.Graph(id='capacitaciones-por-curso'),
            
            # Sección de búsqueda por DNI
            html.Div([
                html.H2('Búsqueda por DNI'),
                dcc.Input(id='dni-input', type='text', placeholder='Ingrese DNI (8 dígitos)'),
                html.Button('Buscar', id='buscar-btn'),
                html.Div(id='dni-error-message', style={'color': 'red'}),
                html.Div(id='dni-results')
            ])
        ])

    ])

    return layout


