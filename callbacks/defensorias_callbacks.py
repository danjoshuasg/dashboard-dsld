from dash import Input, Output, State, dash_table
import plotly.express as px
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
from sqlalchemy import text


# Callbacks para cargar opciones iniciales
@app.callback(Output('dpto-dna-dropdown', 'options'),
              Input('dpto-dna-dropdown', 'search_value'))

def load_dptos(search_value):
    query = "SELECT DISTINCT \"dpto\" FROM dna ORDER BY \"dpto\""
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['dpto']]

@app.callback(Output('estado-dna-dropdown', 'options'),
              Input('estado-dna-dropdown', 'search_value'))
def load_estados(search_value):
    query = "SELECT DISTINCT \"estado_acreditacion\" FROM dna ORDER BY \"estado_acreditacion\""
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['estado_acreditacion']]

# Callbacks para actualizar los dropdowns
@app.callback(Output('prov-dna-dropdown', 'options'),
              Input('dpto-dna-dropdown', 'value'))
def set_provincias_options(selected_dpto):
    if selected_dpto:
        query = "SELECT DISTINCT \"prov\" FROM dna WHERE \"dpto\" = :dpto ORDER BY \"prov\""
        df = run_query(query, {'dpto': selected_dpto})
        return [{'label': i, 'value': i} for i in df['prov']]
    return []

@app.callback(Output('dist-dna-dropdown', 'options'),
              Input('prov-dna-dropdown', 'value'),
              State('dpto-dna-dropdown', 'value'))
def set_distritos_options(selected_prov, selected_dpto):
    if selected_prov and selected_dpto:
        query = "SELECT DISTINCT \"dist\" FROM dna WHERE \"dpto\" = :dpto AND \"prov\" = :prov ORDER BY \"dist\""
        df = run_query(query, {'dpto': selected_dpto, 'prov': selected_prov})
        return [{'label': i, 'value': i} for i in df['dist']]
    return []
# Callback para actualizar los gráficos
@app.callback(
    [Output('dna-por-ubicacion', 'figure'),
     Output('dna-por-estado', 'figure')],
    [Input('dpto-dna-dropdown', 'value'),
     Input('prov-dna-dropdown', 'value'),
     Input('dist-dna-dropdown', 'value'),
     Input('estado-dna-dropdown', 'value')]
)
def update_graphs(dpto, prov, dist, estados):
    # Construir la consulta SQL base
    query = "SELECT"
    params = {}
    
    if dist:
        query += " \"dist\" as ubicacion,"
        where_clause = " WHERE \"dpto\" = :dpto AND \"prov\" = :prov AND \"dist\" = :dist"
        params = {'dpto': dpto, 'prov': prov, 'dist': dist}
        title = f'Número de Defensorías en {dist}, {prov}, {dpto}'
    elif prov:
        query += " \"dist\" as ubicacion,"
        where_clause = " WHERE \"dpto\" = :dpto AND \"prov\" = :prov"
        params = {'dpto': dpto, 'prov': prov}
        title = f'Número de Defensorías por Distrito en {prov}, {dpto}'
    elif dpto:
        query += " \"prov\" as ubicacion,"
        where_clause = " WHERE \"dpto\" = :dpto"
        params = {'dpto': dpto}
        title = f'Número de Defensorías por Provincia en {dpto}'
    else:
        query += " \"dpto\" as ubicacion,"
        where_clause = ""
        title = 'Número de Defensorías por Departamento'

    query += " \"estado_acreditacion\", COUNT(*) as count FROM dna" + where_clause

    if estados:
        if where_clause:
            query += " AND"
        else:
            query += " WHERE"
        query += " \"estado_acreditacion\" IN :estados"
        params['estados'] = tuple(estados)

    query += " GROUP BY ubicacion, \"estado_acreditacion\""

    # Ejecutar la consulta
    df = run_query(query, params)

    # Gráfico de capacitaciones por ubicación
    fig_ubicacion = px.bar(df.groupby('ubicacion').sum().reset_index(), 
                           x='ubicacion', y='count',
                           title=title,
                           labels={'ubicacion': 'Ubicación', 'count': 'Número de Capacitaciones'})
    
    # Gráfico de capacitaciones por curso
    fig_curso = px.pie(df, values='count', names='estado_acreditacion', 
                       title='Distribución de Capacitaciones por Estados de Acreditación')

    return fig_ubicacion, fig_curso


from dash import Input, Output, State, dash_table, html
import pandas as pd
from app import app
from utils.data_loader import run_query

@app.callback(
    [Output('dna-results', 'children'),
     Output('dna-error-message', 'children')],
    Input('buscar-dna-btn', 'n_clicks'),
    State('dna-input', 'value'),
    prevent_initial_call=True
)
def buscar_por_dna(n_clicks, codigo):
    if not codigo or not codigo.isdigit() or len(codigo) != 5:
        return None, "El código de la DNA debe contener exactamente 5 dígitos."
    
    query = """
    SELECT 
        modelo AS "Tipo de DNA",
        dpto AS "Departamento",
        prov AS "Provincia",
        dist AS "Distrito",
        estado_acreditacion AS "Estado de Acreditación",
        f_acreditacion AS "Fecha de Acreditación",
        resolución_acreditación AS "Resolución de Acreditación",
        direccion AS "Dirección DNA",
        fono1 AS "Teléfono DNA",
        email AS "Correo electrónico DNA",
        horario AS "Horario de atención",
        f_inicio AS "Fecha Resolución de Creación",
        doc_creacion AS "Resolución de Creación",
        f_rof AS "Fecha Resolución de ROF",
        rof AS "Resolución de ROF",
        estado_registro AS "Estado de Registro",
        f_registro AS "Fecha de Registro",
        resolución_inscripción AS "Resolución de Inscripción",
        def_f AS "Defensoras",
        def_m AS "Defensores",
        promdef_f AS "Promotoras",
        promdef_m AS "Promotores",
        otros_f AS "Otras",
        otros_m AS "Otros",
        f_supervisión AS "Última fecha de supervisión",
        observaciones AS "Observaciones de la supervisión",
        curso AS "Último curso",
        f_curso AS "Fecha del último curso",
        f_cconna AS "Fecha CCONNA",
        fortalecida AS "DNA Fortalecida"
    FROM dna
    WHERE codigo = :codigo
    """
    
    df = run_query(query, {'codigo': codigo})
    
    if df.empty:
        return html.Div("No se encontraron resultados para esta DNA."), None
    
    # Calcular totales de personal
    df['Total Mujeres'] = df['Defensoras'].fillna(0) + df['Promotoras'].fillna(0) + df['Otras'].fillna(0)
    df['Total Hombres'] = df['Defensores'].fillna(0) + df['Promotores'].fillna(0) + df['Otros'].fillna(0)
    
    # Reorganizar las columnas
    column_order = [
        "Tipo de DNA",
        "Departamento", "Provincia", "Distrito",
        "Estado de Acreditación", "Fecha de Acreditación", "Resolución de Acreditación",
        "Dirección DNA", "Teléfono DNA", "Correo electrónico DNA", "Horario de atención",
        "Fecha Resolución de Creación", "Resolución de Creación",
        "Fecha Resolución de ROF", "Resolución de ROF",
        "Estado de Registro", "Fecha de Registro", "Resolución de Inscripción",
        "Defensoras", "Defensores", "Promotoras", "Promotores", "Otras", "Otros",
        "Total Mujeres", "Total Hombres",
        "Última fecha de supervisión", "Observaciones de la supervisión",
        "Último curso", "Fecha del último curso",
        "Fecha CCONNA", "DNA Fortalecida"
    ]
    df = df.reindex(columns=column_order)
    
    # Crear la tabla
    table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'auto'},
        style_cell={
            'minWidth': '150px', 'width': '200px', 'maxWidth': '300px',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'textAlign': 'left'
        },
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        tooltip_data=[
            {column: {'value': str(value), 'type': 'markdown'}
             for column, value in row.items()}
            for row in df.to_dict('records')
        ],
        tooltip_duration=None
    )
    
    return html.Div([html.H3(f"Resultados para DNA {codigo}"), table]), None