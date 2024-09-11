from dash import html
import dash_bootstrap_components as dbc

navbar = html.Div([
    html.Div([
        html.Img(src="/assets/logo.png", style={'width': '80%', 'margin': '10%'}),
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    dbc.Nav([
        dbc.NavLink("Defensorías", href="/defensorias", active="exact"),
        dbc.NavLink("Responsables", href="/responsables", active="exact"),
        dbc.NavLink("Supervisiones", href="/supervisiones", active="exact"),
        dbc.NavLink("Capacitaciones", href="/capacitaciones", active="exact"),
        dbc.NavLink("CCONNA", href="/cconna", active="exact"),
        dbc.NavLink("Modo Niñez", href="/modo_ninez", active="exact"),
    ], vertical=True, pills=True),
    
], style={
    'position': 'fixed',
    'top': 0,
    'left': 0,
    'bottom': 0,
    'width': '250px',
    'padding': '20px',
    'background-color': '#f8f9fa',
    'boxShadow': '2px 0 5px rgba(0,0,0,0.1)'
})