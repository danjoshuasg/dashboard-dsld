import os
from dash.dependencies import Input, Output, State
from dash import html, dcc, callback_context
from app import app, server
from layouts import defensores, defensorias, supervisiones, capacitaciones, cconna, modo_ninez
from components.navbar import navbar
import callbacks.defensorias_callbacks 
import callbacks.capacitaciones_callbacks
import callbacks.defensores_callbacks
import callbacks.cconna_callbacks

# Definir colores
TEXT_COLOR = "#F0F0F0"
ACCENT_COLOR = "#421e1b"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content', style={
        'marginLeft': '250px',
        'padding': '20px',
        'paddingTop': '40px',
        'transition': 'margin-left 0.3s ease-in-out'
    })
])

@app.callback(
    [Output('navbar-content', 'style'),
     Output('page-content', 'style'),
     Output('navbar-toggle', 'style')],
    [Input('navbar-toggle', 'n_clicks')],
    [State('navbar-content', 'style'),
     State('page-content', 'style'),
     State('navbar-toggle', 'style')]
)
def toggle_navbar(n_clicks, navbar_style, content_style, toggle_style):
    if n_clicks is None:
        return navbar_style, content_style, toggle_style
    if navbar_style['transform'] == 'translateX(0)':
        # Ocultar navbar
        navbar_style['transform'] = 'translateX(-250px)'
        content_style['marginLeft'] = '50px'
        toggle_style['left'] = '10px'
        toggle_style['color'] = ACCENT_COLOR  # Cambiar color cuando está oculto
    else:
        # Mostrar navbar
        navbar_style['transform'] = 'translateX(0)'
        content_style['marginLeft'] = '250px'
        toggle_style['left'] = '210px'
        toggle_style['color'] = TEXT_COLOR  # Restaurar color original

    # Añadir transición al estilo del botón
    toggle_style['transition'] = 'left 0.3s ease-in-out, color 0.3s ease-in-out'

    return navbar_style, content_style, toggle_style

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/defensorias' or pathname == '/':
        return defensorias.get_layout()
    elif pathname == '/defensores':
        return defensores.get_layout()
    elif pathname == '/supervisiones':
        return supervisiones.get_layout()
    elif pathname == '/capacitaciones':
        return capacitaciones.get_layout()
    elif pathname == '/cconna':
        return cconna.get_layout()
    elif pathname == '/modo_ninez':
        return modo_ninez.get_layout()
    else:
        return html.H1('404: Página no encontrada')

if __name__ == '__main__':
    app.run_server(debug=True)
    #port = int(os.environ.get('PORT', 8050))
    #app.run_server(host='0.0.0.0', port=port, debug=True)