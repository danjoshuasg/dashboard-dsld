from dash import html
import dash_bootstrap_components as dbc
from app import app

# Definimos algunos colores como variables para facilitar su uso y modificación
BACKGROUND_COLOR = "#421e1b"  # Un fondo oscuro tipo burdeos
TEXT_COLOR = "#F0F0F0"  # Un blanco más suave con un toque cálido
ACCENT_COLOR = "#748CAB"  # Un azul grisáceo más suave y refinado
HOVER_COLOR = "#FFD966"  # Un azul claro más sutil para el hover
ACTIVE_COLOR = "#FFD966"  # Un dorado suave para los NavLinks activos

# Estilos para los NavLinks
navlink_style = {
    'color': TEXT_COLOR,
    'transition': 'all 0.3s ease',
    'borderRadius': '5px',
    'margin': '5px 0',
    'padding': '10px 15px',
    'width': '100%',
    'textAlign': 'left',
    'display': 'flex',
    'alignItems': 'center',
}

navbar = html.Div([
    html.Button(
        html.I(className="fas fa-bars"),
        id='navbar-toggle',
        style={
            'position': 'fixed',
            'top': '10px',
            'left': '210px',
            'zIndex': 1060,
            'background': 'none',
            'border': 'none',
            'fontSize': '20px',
            'color': TEXT_COLOR,
            'cursor': 'pointer',
            'padding': '5px',
            'transition': 'left 0.3s ease-in-out, color 0.3s ease-in-out'
        }
    ),
    html.Div([
        html.Div([
            html.Img(src="/assets/logo.png", style={
                'width': '120px',
                'height': '120px',
                'borderRadius': '50%',
                'objectFit': 'cover',
                'marginBottom': '20px',
                'display': 'block',
                'marginLeft': 'auto',
                'marginRight': 'auto'
            })
        ], style={
            'textAlign': 'center',
            'width': '100%'
        }),
        dbc.Nav([
            dbc.NavLink([
                html.I(className="fas fa-shield-alt", style={'marginRight': '10px'}),
                "Defensorías"
            ], href="/defensorias", active="exact", style=navlink_style, className="custom-navlink"),
            dbc.NavLink([
                html.I(className="fas fa-user-tie", style={'marginRight': '10px'}),
                "Defensores"
            ], href="/defensores", active="exact", style=navlink_style, className="custom-navlink"),
            dbc.NavLink([
                html.I(className="fas fa-clipboard-check", style={'marginRight': '10px'}),
                "Supervisiones"
            ], href="/supervisiones", active="exact", style=navlink_style, className="custom-navlink"),
            dbc.NavLink([
                html.I(className="fas fa-graduation-cap", style={'marginRight': '10px'}),
                "Capacitaciones"
            ], href="/capacitaciones", active="exact", style=navlink_style, className="custom-navlink"),
            dbc.NavLink([
                html.I(className="fas fa-comments", style={'marginRight': '10px'}),
                "CCONNA"
            ], href="/cconna", active="exact", style=navlink_style, className="custom-navlink"),
            dbc.NavLink([
                html.I(className="fas fa-child", style={'marginRight': '10px'}),
                "Modo Niñez"
            ], href="/modo_ninez", active="exact", style=navlink_style, className="custom-navlink"),
        ], vertical=True, pills=True, style={
            'width': '100%',
        }),
        html.Div([
            html.P("DSLD-MIMP 2024", style={'marginBottom': '5px', 'color': TEXT_COLOR}),
        ], style={
            'position': 'absolute',
            'bottom': '20px',
            'left': '0',
            'right': '0',
            'textAlign': 'center',
            'fontSize': '12px'
        })
    ], id='navbar-content', style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '250px',
        'padding': '20px',
        'paddingTop': '50px',
        'backgroundColor': BACKGROUND_COLOR,
        'color': TEXT_COLOR,
        'boxShadow': '2px 0 5px rgba(0,0,0,0.1)',
        'zIndex': 1050,
        'transform': 'translateX(0)',
        'transition': 'transform 0.3s ease-in-out',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center'
    })
])

# Definir estilos CSS personalizados inline
custom_styles = f"""
<style>
.custom-navlink.active {{
    background-color: {ACTIVE_COLOR} !important;
    color: {BACKGROUND_COLOR} !important;
}}
.custom-navlink:hover {{
    color: {HOVER_COLOR} !important;
    background-color: rgba(255, 255, 255, 0.1) !important;
}}
</style>
"""

# Añadir los estilos CSS personalizados al layout de la aplicación
app.index_string = app.index_string.replace(
    '</head>',
    custom_styles + '</head>'
)