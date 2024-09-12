from dash import html
import dash_bootstrap_components as dbc

navbar = html.Div([
    html.Button(
        html.I(className="fas fa-bars"),  # Icono inicial de barras
        id='navbar-toggle',
        style={
            'position': 'fixed',
            'top': '10px',
            'left': '210px',
            'zIndex': 1060,
            'background': 'none',
            'border': 'none',
            'fontSize': '20px',
            'color': '#007bff',
            'cursor': 'pointer',
            'padding': '5px',
            'transition': 'left 0.3s ease-in-out'
        }
    ),
    html.Div([
        html.Div([
            html.Img(src="/assets/logo.png", style={
                'width': '120px',  # Tamaño fijo para el logo
                'height': '120px',  # Asegura que sea cuadrado
                'borderRadius': '50%',  # Hace la imagen circular
                'objectFit': 'cover',  # Asegura que la imagen cubra todo el espacio
                'marginBottom': '20px',
                'display': 'block',  # Necesario para el margen automático
                'marginLeft': 'auto',
                'marginRight': 'auto'
            })
        ], style={
            'textAlign': 'center',  # Centra el contenido del div
            'width': '100%'  # Asegura que el div ocupe todo el ancho disponible
        }),
        dbc.Nav([
            dbc.NavLink("Defensorías", href="/defensorias", active="exact"),
            dbc.NavLink("Responsables", href="/responsables", active="exact"),
            #dbc.NavLink("Supervisiones", href="/supervisiones", active="exact"),
            dbc.NavLink("Capacitaciones", href="/capacitaciones", active="exact"),
            #dbc.NavLink("CCONNA", href="/cconna", active="exact"),
            #dbc.NavLink("Modo Niñez", href="/modo_ninez", active="exact"),
        ], vertical=True, pills=True),
    ], id='navbar-content', style={
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'bottom': 0,
        'width': '250px',
        'padding': '20px',
        'paddingTop': '50px',  # Aumentado para dejar espacio al botón
        'background-color': '#f8f9fa',
        'boxShadow': '2px 0 5px rgba(0,0,0,0.1)',
        'zIndex': 1050,
        'transform': 'translateX(0)',  # Estado inicial de la barra visible
        'transition': 'transform 0.3s ease-in-out',
        'display': 'flex',  # Utilizamos flexbox para el centrado vertical
        'flexDirection': 'column',  # Los elementos se apilan verticalmente
        'alignItems': 'center'  # Centra los elementos horizontalmente
    })
])