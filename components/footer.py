from dash import html
import dash_bootstrap_components as dbc

footer = html.Footer([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Span("DSLD - 2024"), width=6),
            dbc.Col(
                html.A("Web del Ministerio", href="https://www.gob.pe/mimp", target="_blank"),
                width=6,
                className="text-right"
            ),
        ]),
    ]),
], style={
    'position': 'fixed',
    'bottom': 0,
    'left': '250px',  # Ajusta esto al ancho de tu navbar
    'right': 0,
    'padding': '10px',
    'background-color': '#f8f9fa',
    'borderTop': '1px solid #dee2e6',
    'textAlign': 'center'
})