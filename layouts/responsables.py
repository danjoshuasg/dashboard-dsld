from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

def get_layout():
    layout = html.Div([
        dbc.Container([
            html.H1('Visualizador de Datos de los defensores de las DNA', className='text-center my-4 display-4'),
            
            dbc.Card([
                dbc.CardBody([
                    html.H2('Selección de los defensores', className='card-title mb-3'),
                    dbc.Row([
                        dbc.Col([
                            html.Label('Departamento:', className='fw-bold'),
                            #dcc.Dropdown(id='dpto-defensores-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Provincia:', className='fw-bold'),
                            #dcc.Dropdown(id='prov-defensores-dropdown', className='mb-2'),
                        ], md=4),
                        dbc.Col([
                            html.Label('Distrito:', className='fw-bold'),
                            #dcc.Dropdown(id='dist-defensores-dropdown', className='mb-2'),
                        ], md=4),   
                    ], className='mb-3'),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Label('Estado de Acreditación:', className='fw-bold'),
                            #dcc.Dropdown(id='estado-dna-dropdown', multi=True, className='mb-2'),
                        ], md=6),
                        dbc.Col([
                            html.Label('Tipo de DNA:', className='fw-bold'),
                            #dcc.Dropdown(id='tipo-dna-dropdown', multi=True, className='mb-2'),
                        ], md=6),
                    ], className='mb-3'),
                    
                    dbc.Row([
                        #dbc.Col(dcc.Graph(id='dna-por-ubicacion'), width=12, className='mb-3'),
                    ]),
                    
                    dbc.Row([
                        #dbc.Col(dcc.Graph(id='dna-por-estado'), md=6, className='mb-3'),
                        #dbc.Col(dcc.Graph(id='dna-por-tipo'), md=6, className='mb-3'),
                    ]),
                ])
            ], className='mb-4 shadow'),
        ])
    ])

    return layout