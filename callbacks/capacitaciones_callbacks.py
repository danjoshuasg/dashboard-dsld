from dash import Input, Output, State, dash_table
import plotly.express as px
from app import app
from utils.data_loader import run_query

# Callbacks para cargar opciones iniciales
@app.callback(Output('dpto-capacitaciones-dropdown', 'options'),
              Input('dpto-capacitaciones-dropdown', 'search_value'))

def load_dptos(search_value):
    query = "SELECT DISTINCT \"DEPARTAMENTO\" FROM capacitaciones ORDER BY \"DEPARTAMENTO\""
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['DEPARTAMENTO']]

@app.callback(Output('curso-capacitaciones-dropdown', 'options'),
              Input('curso-capacitaciones-dropdown', 'search_value'))
def load_cursos(search_value):
    query = "SELECT DISTINCT \"CURSO\" FROM capacitaciones ORDER BY \"CURSO\""
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['CURSO']]

# Callbacks para actualizar los dropdowns
@app.callback(Output('prov-capacitaciones-dropdown', 'options'),
              Input('dpto-capacitaciones-dropdown', 'value'))
def set_provincias_options(selected_dpto):
    if selected_dpto:
        query = "SELECT DISTINCT \"PROVINCIA\" FROM capacitaciones WHERE \"DEPARTAMENTO\" = :dpto ORDER BY \"PROVINCIA\""
        df = run_query(query, {'dpto': selected_dpto})
        return [{'label': i, 'value': i} for i in df['PROVINCIA']]
    return []

@app.callback(Output('dist-capacitaciones-dropdown', 'options'),
              Input('prov-capacitaciones-dropdown', 'value'),
              State('dpto-capacitaciones-dropdown', 'value'))
def set_distritos_options(selected_prov, selected_dpto):
    if selected_prov and selected_dpto:
        query = "SELECT DISTINCT \"DISTRITO\" FROM capacitaciones WHERE \"DEPARTAMENTO\" = :dpto AND \"PROVINCIA\" = :prov ORDER BY \"DISTRITO\""
        df = run_query(query, {'dpto': selected_dpto, 'prov': selected_prov})
        return [{'label': i, 'value': i} for i in df['DISTRITO']]
    return []

# Callback para actualizar los gráficos
@app.callback(
    [Output('capacitaciones-por-ubicacion', 'figure'),
     Output('capacitaciones-por-curso', 'figure')],
    [Input('dpto-capacitaciones-dropdown', 'value'),
     Input('prov-capacitaciones-dropdown', 'value'),
     Input('dist-capacitaciones-dropdown', 'value'),
     Input('curso-capacitaciones-dropdown', 'value')]
)
def update_graphs(dpto, prov, dist, cursos):
    # Construir la consulta SQL base
    query = "SELECT"
    params = {}
    
    if dist:
        query += " \"DISTRITO\" as ubicacion,"
        where_clause = " WHERE \"DEPARTAMENTO\" = :dpto AND \"PROVINCIA\" = :prov AND \"DISTRITO\" = :dist"
        params = {'dpto': dpto, 'prov': prov, 'dist': dist}
        title = f'Número de Capacitaciones en {dist}, {prov}, {dpto}'
    elif prov:
        query += " \"DISTRITO\" as ubicacion,"
        where_clause = " WHERE \"DEPARTAMENTO\" = :dpto AND \"PROVINCIA\" = :prov"
        params = {'dpto': dpto, 'prov': prov}
        title = f'Número de Capacitaciones por Distrito en {prov}, {dpto}'
    elif dpto:
        query += " \"PROVINCIA\" as ubicacion,"
        where_clause = " WHERE \"DEPARTAMENTO\" = :dpto"
        params = {'dpto': dpto}
        title = f'Número de Capacitaciones por Provincia en {dpto}'
    else:
        query += " \"DEPARTAMENTO\" as ubicacion,"
        where_clause = ""
        title = 'Número de Capacitaciones por Departamento'

    query += " \"CURSO\", COUNT(*) as count FROM capacitaciones" + where_clause

    if cursos:
        if where_clause:
            query += " AND"
        else:
            query += " WHERE"
        query += " \"CURSO\" IN :cursos"
        params['cursos'] = tuple(cursos)

    query += " GROUP BY ubicacion, \"CURSO\""

    # Ejecutar la consulta
    df = run_query(query, params)

    # Gráfico de capacitaciones por ubicación
    fig_ubicacion = px.bar(df.groupby('ubicacion').sum().reset_index(), 
                           x='ubicacion', y='count',
                           title=title,
                           labels={'ubicacion': 'Ubicación', 'count': 'Número de Capacitaciones'})
    
    # Gráfico de capacitaciones por curso
    fig_curso = px.pie(df, values='count', names='CURSO', 
                       title='Distribución de Capacitaciones por Curso')

    return fig_ubicacion, fig_curso

# Callback para la búsqueda por DNI
@app.callback(
    [Output('dni-results', 'children'),
     Output('dni-error-message', 'children')],
    Input('buscar-btn', 'n_clicks'),
    State('dni-input', 'value'),
    prevent_initial_call=True
)
def buscar_por_dni(n_clicks, dni):
    if not dni or not dni.isdigit() or len(dni) != 8:
        return None, "El DNI debe contener exactamente 8 dígitos."
    
    query = """
    SELECT "AÑO", "CURSO", "DEPARTAMENTO", "PROVINCIA", "DISTRITO", "SEDE DE CAPACITACIÓN", 
           "FECHA INICIO CURSO", "FECHA CULMINA CURSO", "NOTA OBTENIDA", "CONDICIÓN"
    FROM capacitaciones
    WHERE "DNI" = :dni
    ORDER BY "AÑO" DESC, "FECHA INICIO CURSO" DESC
    """
    
    df = run_query(query, {'dni': dni})
    
    if df.empty:
        return "No se encontraron resultados para este DNI.", None
    
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'minWidth': '100px', 'width': '150px', 'maxWidth': '300px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        }
    )
    
    return table, None