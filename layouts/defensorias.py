from dash import html, dcc
import dash_bootstrap_components as dbc

def get_layout():
    layout = dbc.Container([
        html.Div([
            html.H1('Dashboard de Defensorías'),
            
            # Filtros en cascada
            html.Div([
                html.Label('Seleccionar Departamento:'),
                dcc.Dropdown(id='dpto-dna-dropdown'),
                html.Label('Seleccionar Provincia:'),
                dcc.Dropdown(id='prov-dna-dropdown'),
                html.Label('Seleccionar Distrito:'),
                dcc.Dropdown(id='dist-dna-dropdown'),
            ]),
            
            html.Div([
                html.Label('Filtrar por Estado de Acreditación:'),
                dcc.Dropdown(id='estado-dna-dropdown', multi=True)
            ]),
            
            # Gráficos
            dcc.Graph(id='dna-por-ubicacion'),
            dcc.Graph(id='dna-por-estado'),
            
            # Sección de búsqueda por código de DNA
            html.Div([
                html.H2('Búsqueda por Código de DNA'),
                dcc.Input(id='dna-input', type='text', placeholder='Ingrese Código de DNA'),
                html.Button('Buscar', id='buscar-dna-btn'),
                html.Div(id='dna-error-message', style={'color': 'red'}),
                html.Div(id='dna-results')
            ])
        ])
    ])
    
    return layout