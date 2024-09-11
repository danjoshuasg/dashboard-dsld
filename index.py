import os
from dash import html, dcc
from dash.dependencies import Input, Output
from app import app, server
from layouts import defensorias, responsables, supervisiones, capacitaciones,cconna, modo_ninez
from components.navbar import navbar
import callbacks.defensorias_callbacks 
import callbacks.capacitaciones_callbacks


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/defensorias' or pathname == '/':
        return defensorias.get_layout()
    elif pathname == '/responsables':
        return responsables.layout
    elif pathname == '/supervisiones':
        return supervisiones.layout
    elif pathname == '/capacitaciones':
        return capacitaciones.get_layout()
    elif pathname == '/cconna':
        return cconna.get_layout()
    elif pathname == '/modo_ninez':
        return modo_ninez.get_layout()
    else:
        return html.H1('404: Página no encontrada')

if __name__ == '__main__':
    #app.run_server(debug=True)
    port = int(os.environ.get('PORT', 8050))
    app.run_server(host='0.0.0.0', port=port, debug=True)