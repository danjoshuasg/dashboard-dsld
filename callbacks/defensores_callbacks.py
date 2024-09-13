from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
from sqlalchemy import text
import math

colores_seaborn = px.colors.qualitative.Set2

# Callbacks para cargar opciones iniciales
@app.callback(Output('dpto-defensores-dropdown', 'options'),
              Input('dpto-defensores-dropdown', 'search_value'))

def load_dptos(search_value):
    query = "SELECT DISTINCT \"dpto\" FROM dna ORDER BY \"dpto\""
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['dpto']]

# Callbacks para actualizar los dropdowns
@app.callback(Output('prov-defensores-dropdown', 'options'),
              Input('dpto-defensores-dropdown', 'value'))
def set_provincias_options(selected_dpto):
    if selected_dpto:
        query = "SELECT DISTINCT \"prov\" FROM dna WHERE \"dpto\" = :dpto ORDER BY \"prov\""
        df = run_query(query, {'dpto': selected_dpto})
        return [{'label': i, 'value': i} for i in df['prov']]
    return []

@app.callback(Output('dist-defensores-dropdown', 'options'),
              Input('prov-defensores-dropdown', 'value'),
              State('dpto-defensores-dropdown', 'value'))
def set_distritos_options(selected_prov, selected_dpto):
    if selected_prov and selected_dpto:
        query = "SELECT DISTINCT \"dist\" FROM dna WHERE \"dpto\" = :dpto AND \"prov\" = :prov ORDER BY \"dist\""
        df = run_query(query, {'dpto': selected_dpto, 'prov': selected_prov})
        return [{'label': i, 'value': i} for i in df['dist']]
    return []

# Callbacks para estados de DNA
@app.callback(
    Output('cargo-defensores-dropdown', 'options'),
    Input('cargo-defensores-dropdown', 'search_value')
)
def load_cargos(search_value):
    query = """
    SELECT DISTINCT e.descripcion 
    FROM cargo e
    JOIN defensores d ON e.codigo = d.cargo
    ORDER BY e.descripcion
    """
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['descripcion']]

# Valores por defecto de los estados de DNA
@app.callback(
    Output('cargo-defensores-dropdown', 'value'),
    Input('cargo-defensores-dropdown', 'options')
)
def set_cargos_default(available_options):
    default_values = ['Responsable', 'Defensor']
    return [option['value'] for option in available_options if option['label'] in default_values]

# Callbacks para estados de DNA
@app.callback(
    Output('ocupacion-defensores-dropdown', 'options'),
    Input('ocupacion-defensores-dropdown', 'search_value')
)
def load_ocupaciones(search_value):
    query = """
    SELECT DISTINCT m.ocupacion 
    FROM ocupacion m
    JOIN defensores d ON m.codigo = d.ocupacion
    ORDER BY m.ocupacion
    """
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['ocupacion']]

@app.callback(
    [Output('defensores-por-ubicacion', 'figure'),        
    Output('defensores-por-cargo', 'figure'),
     Output('defensores-por-ocupacion', 'figure')],
    [Input('dpto-defensores-dropdown', 'value'),
     Input('prov-defensores-dropdown', 'value'),
     Input('dist-defensores-dropdown', 'value'),
     Input('cargo-defensores-dropdown', 'value'),
     Input('ocupacion-defensores-dropdown', 'value')]
)
def update_graphs(dpto, prov, dist, cargos, ocupaciones):
    # Construir la consulta SQL base
    query = """
    SELECT 
        CASE
            WHEN :dist IS NOT NULL THEN dna.dist
            WHEN :prov IS NOT NULL THEN dna.dist
            WHEN :dpto IS NOT NULL THEN dna.prov
            ELSE dna.dpto
        END as ubicacion,
        c.descripcion as cargo,
        o.ocupacion as ocupacion,
        COUNT(*) as count
    FROM defensores d
    JOIN dna ON d.codigo_dna = dna.codigo
    JOIN cargo c ON d.cargo = c.codigo
    JOIN ocupacion o ON d.ocupacion = o.codigo
    """
    
    where_clauses = []
    params = {'dpto': dpto, 'prov': prov, 'dist': dist}
    
    if dist:
        where_clauses.append("dna.dpto = :dpto AND dna.prov = :prov AND dna.dist = :dist")
    elif prov:
        where_clauses.append("dna.dpto = :dpto AND dna.prov = :prov")
    elif dpto:
        where_clauses.append("dna.dpto = :dpto")
    
    if cargos:
        where_clauses.append("c.descripcion IN :cargos")
        params['cargos'] = tuple(cargos)
    
    if ocupaciones:
        where_clauses.append("o.ocupacion IN :ocupaciones")
        params['ocupaciones'] = tuple(ocupaciones)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += """
    GROUP BY 
        CASE
            WHEN :dist IS NOT NULL THEN dna.dist
            WHEN :prov IS NOT NULL THEN dna.dist
            WHEN :dpto IS NOT NULL THEN dna.prov
            ELSE dna.dpto
        END,
        c.descripcion,
        o.ocupacion
    """

    # Ejecutar la consulta
    df = run_query(query, params)
    
    # Calcular el total
    total = df['count'].sum()

    # Construir el título basado en los filtros aplicados
    if dist:
        title = f'Número de Defensores en {dist}, {prov}, {dpto}: {total}'
    elif prov:
        title = f'Número de Defensores por Distrito en {prov}, {dpto}: {total}'
    elif dpto:
        title = f'Número de Defensores por Provincia en {dpto}: {total}'
    else:
        title = f'Número de Defensores por Departamento: {total}'

    # Gráfico de defensores por ubicación
    fig_ubicacion = px.bar(df.groupby('ubicacion').sum().reset_index(), 
                        x='ubicacion', y='count',
                        title=title,
                        labels={'ubicacion': 'Ubicación', 'count': 'Número de Defensores'},
                        color_discrete_sequence=colores_seaborn)

    # Gráfico de defensores por cargo
    fig_cargo = px.pie(df.groupby('cargo').sum().reset_index(), 
                        values='count', names='cargo', 
                        title=f'Distribución de Defensores por Cargo',
                        color_discrete_sequence=colores_seaborn)
    
    # Configurar la leyenda para que aparezca debajo del gráfico
    fig_cargo.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )

    # Gráfico de defensores por ocupación
    fig_ocupacion = px.pie(df.groupby('ocupacion').sum().reset_index(), 
                        values='count', names='ocupacion', 
                        title=f'Distribución de Defensores por Ocupación',
                        color_discrete_sequence=colores_seaborn)
    
    # Configurar la leyenda para que aparezca debajo del gráfico
    fig_ocupacion.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=-0.5, xanchor="center", x=0.5)
    )

    # Personalización adicional para mejorar la apariencia
    for fig in [fig_ubicacion, fig_cargo, fig_ocupacion]:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12),
        )
    
    # Para el gráfico de barras, añadimos algunas personalizaciones específicas
    fig_ubicacion.update_xaxes(tickangle=-45)
    fig_ubicacion.update_yaxes(gridcolor='lightgray')


    return fig_ubicacion, fig_cargo, fig_ocupacion

@app.callback(
    [Output('tabla-defensores', 'data'),
     Output('tabla-defensores', 'page_count'),
     Output('pagination-defensores', 'max_value')],
    [Input('dpto-defensores-dropdown', 'value'),
     Input('prov-defensores-dropdown', 'value'),
     Input('dist-defensores-dropdown', 'value'),
     Input('cargo-defensores-dropdown', 'value'),
     Input('ocupacion-defensores-dropdown', 'value'),
     Input('tabla-defensores', 'page_current'),
     Input('tabla-defensores', 'page_size')]
)
def update_tabla_defensores(dpto, prov, dist, cargos, ocupaciones, page_current, page_size):
    # Construir la consulta SQL base
    query = """
    SELECT d.codigo_dna, d.nombres, d.apellido, c.descripcion as cargo, d.dni, o.ocupacion
    FROM defensores d
    JOIN dna ON d.codigo_dna = dna.codigo
    JOIN cargo c ON d.cargo = c.codigo
    JOIN ocupacion o ON d.ocupacion = o.codigo
    """
    
    where_clauses = []
    params = {'dpto': dpto, 'prov': prov, 'dist': dist}
    
    if dist:
        where_clauses.append("dna.dpto = :dpto AND dna.prov = :prov AND dna.dist = :dist")
    elif prov:
        where_clauses.append("dna.dpto = :dpto AND dna.prov = :prov")
    elif dpto:
        where_clauses.append("dna.dpto = :dpto")
    
    if cargos:
        where_clauses.append("c.descripcion IN :cargos")
        params['cargos'] = tuple(cargos)
    
    if ocupaciones:
        where_clauses.append("o.ocupacion IN :ocupaciones")
        params['ocupaciones'] = tuple(ocupaciones)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    # Agregar ordenamiento y paginación
    query += " ORDER BY d.apellido, d.nombres"
    query += f" LIMIT {page_size} OFFSET {page_current * page_size}"
    
    # Ejecutar la consulta
    df = run_query(query, params)
    
    # Obtener el conteo total de registros para la paginación
    count_query = f"SELECT COUNT(*) as total FROM ({query.split('ORDER BY')[0]}) as subquery"
    total_records = run_query(count_query, params).iloc[0]['total']
    
    # Calcular el número total de páginas
    total_pages = math.ceil(total_records / page_size)
    
    return df.to_dict('records'), total_pages, total_pages

@app.callback(
    Output('nombramientos-acumulados', 'figure'),
    [Input('fecha-inicio', 'date'),
     Input('fecha-fin', 'date'),
     Input('dpto-defensores-dropdown', 'value'),
     Input('prov-defensores-dropdown', 'value'),
     Input('dist-defensores-dropdown', 'value')]
)
def update_nombramientos_acumulados_graph(fecha_inicio, fecha_fin, dpto, prov, dist):
    # Convertir las fechas a objetos datetime
    fecha_inicio = pd.to_datetime(fecha_inicio)
    fecha_fin = pd.to_datetime(fecha_fin)

    # Construir la consulta SQL
    query = """
    SELECT d.f_nombramiento AS fecha
    FROM defensores d
    JOIN dna ON d.codigo_dna = dna.codigo
    WHERE d.f_nombramiento BETWEEN :fecha_inicio AND :fecha_fin
    """
    
    params = {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
    
    # Agregar filtros de ubicación si están presentes
    if dist:
        query += " AND dna.dpto = :dpto AND dna.prov = :prov AND dna.dist = :dist"
        params.update({'dpto': dpto, 'prov': prov, 'dist': dist})
    elif prov:
        query += " AND dna.dpto = :dpto AND dna.prov = :prov"
        params.update({'dpto': dpto, 'prov': prov})
    elif dpto:
        query += " AND dna.dpto = :dpto"
        params.update({'dpto': dpto})
    
    query += " ORDER BY d.f_nombramiento"

    # Ejecutar la consulta
    df = run_query(query, params)

    # Convertir la columna de fecha a datetime
    df['fecha'] = pd.to_datetime(df['fecha'])

    # Crear una serie de fechas desde el inicio hasta el fin
    fecha_rango = pd.date_range(start=fecha_inicio, end=fecha_fin, freq='D')

    # Contar nombramientos acumulados por día
    nombramientos_acumulados = df['fecha'].value_counts().sort_index().cumsum()

    # Crear un DataFrame con todas las fechas y los nombramientos acumulados
    df_acumulado = pd.DataFrame({'fecha': fecha_rango})
    df_acumulado['nombramientos_acumulados'] = df_acumulado['fecha'].map(nombramientos_acumulados).fillna(method='ffill').fillna(0)

    # Crear la gráfica
    fig = px.line(df_acumulado, x='fecha', y='nombramientos_acumulados', 
                  title='Evolución Histórica Acumulada de Nombramientos',
                  labels={'fecha': 'Fecha', 'nombramientos_acumulados': 'Nombramientos Acumulados'},
                  line_shape='linear')

    # Personalizar la apariencia
    fig.update_layout(
        xaxis_title='Fecha',
        yaxis_title='Nombramientos Acumulados',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
    )
    fig.update_xaxes(gridcolor='lightgray')
    fig.update_yaxes(gridcolor='lightgray')

    return fig

@app.callback(
    [Output('defensor-results', 'children'),
     Output('defensor-error-message', 'children')],
    [Input('buscar-defensor-btn', 'n_clicks')],
    [State('defensor-input', 'value')]
)
def buscar_defensor(n_clicks, search_value):
    if n_clicks is None or not search_value:
        return None, None
    
    # Construir la consulta SQL
    query = """
    SELECT d.codigo_dna, d.nombres, d.apellido, c.descripcion as cargo, d.dni, o.ocupacion,
           dna.dpto, dna.prov, dna.dist
    FROM defensores d
    JOIN dna ON d.codigo_dna = dna.codigo
    JOIN cargo c ON d.cargo = c.codigo
    JOIN ocupacion o ON d.ocupacion = o.codigo
    WHERE d.nombres ILIKE :search
       OR d.apellido ILIKE :search
       OR d.dni = :dni
    LIMIT 10
    """
    
    params = {
        'search': f'%{search_value}%',
        'dni': search_value if search_value.isdigit() else None
    }
    
    # Ejecutar la consulta
    df = run_query(query, params)
    
    if df.empty:
        return None, "No se encontraron defensores con los criterios de búsqueda proporcionados."
    
    # Crear una lista de tarjetas con la información de los defensores
    defensor_cards = []
    for _, row in df.iterrows():
        card = dbc.Card(
            dbc.CardBody([
                html.H5(f"{row['nombres']} {row['apellido']}", className="card-title"),
                html.P(f"DNI: {row['dni']}", className="card-text"),
                html.P(f"Cargo: {row['cargo']}", className="card-text"),
                html.P(f"Ocupación: {row['ocupacion']}", className="card-text"),
                html.P(f"Ubicación: {row['dist']}, {row['prov']}, {row['dpto']}", className="card-text"),
                html.P(f"Código DNA: {row['codigo_dna']}", className="card-text"),
            ]),
            className="mb-3"
        )
        defensor_cards.append(card)
    
    return defensor_cards, None
