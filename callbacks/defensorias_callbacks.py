from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
from sqlalchemy import text

colores_seaborn = px.colors.qualitative.Set2

# Callbacks para cargar opciones iniciales
@app.callback(Output('dpto-dna-dropdown', 'options'),
              Input('dpto-dna-dropdown', 'search_value'))

def load_dptos(search_value):
    query = "SELECT DISTINCT \"dpto\" FROM dna ORDER BY \"dpto\""
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['dpto']]
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

# Callbacks para estados de DNA
@app.callback(
    Output('estado-dna-dropdown', 'options'),
    Input('estado-dna-dropdown', 'search_value')
)
def load_estados(search_value):
    query = """
    SELECT DISTINCT e.estado 
    FROM estadodna e
    JOIN dna d ON e.codigo = d.estado_acreditacion
    ORDER BY e.estado
    """
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['estado']]

# Valores por defecto de los estados de DNA
@app.callback(
    Output('estado-dna-dropdown', 'value'),
    Input('estado-dna-dropdown', 'options')
)
def set_estado_default(available_options):
    default_values = ['Acreditada', 'No acreditada', 'No operativa']
    return [option['value'] for option in available_options if option['label'] in default_values]
    
# Callbacks para tipos de DNA
@app.callback(
    Output('tipo-dna-dropdown', 'options'),
    Input('tipo-dna-dropdown', 'search_value')
)
def load_tipos(search_value):
    # Cambia "estadodna" por el nombre correcto de la tabla que contiene "siglas", por ejemplo "modelodna"
    query = """
    SELECT DISTINCT m.siglas 
    FROM modelodna m  -- Cambia "estadodna" por "modelodna"
    JOIN dna d ON m.codigo = d.modelo
    ORDER BY m.siglas
    """
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['siglas']]

# Valores por defecto de los tipos de DNA
@app.callback(
    Output('tipo-dna-dropdown', 'value'),
    Input('tipo-dna-dropdown', 'options')
)
def set_tipo_default(available_options):
    default_values = ['Distrital', 'Provincial']
    return [option['value'] for option in available_options if option['label'] in default_values]




@app.callback(
    [Output('dna-por-ubicacion', 'figure'),        
    Output('dna-por-estado', 'figure'),
     Output('dna-por-tipo', 'figure')],
    [Input('dpto-dna-dropdown', 'value'),
     Input('prov-dna-dropdown', 'value'),
     Input('dist-dna-dropdown', 'value'),
     Input('estado-dna-dropdown', 'value'),
     Input('tipo-dna-dropdown', 'value')]
)
def update_graphs(dpto, prov, dist, estados, tipos):
    # Construir la consulta SQL base
    query = "SELECT"
    params = {}
    
    # Función para obtener el total
    def get_total(where_clause, params):
        total_query = f"""
            SELECT COUNT(*) as total 
            FROM dna d
            JOIN estadodna e ON d.estado_acreditacion = e.codigo 
            JOIN modelodna m ON d.modelo = m.codigo
            {where_clause}
        """
        total_df = run_query(total_query, params)
        return total_df['total'].iloc[0]
    
    if dist:
        query += " d.\"dist\" as ubicacion,"
        where_clause = " WHERE d.\"dpto\" = :dpto AND d.\"prov\" = :prov AND d.\"dist\" = :dist"
        params = {'dpto': dpto, 'prov': prov, 'dist': dist}
    elif prov:
        query += " d.\"dist\" as ubicacion,"
        where_clause = " WHERE d.\"dpto\" = :dpto AND d.\"prov\" = :prov"
        params = {'dpto': dpto, 'prov': prov}
    elif dpto:
        query += " d.\"prov\" as ubicacion,"
        where_clause = " WHERE d.\"dpto\" = :dpto"
        params = {'dpto': dpto}
    else:
        query += " d.\"dpto\" as ubicacion,"
        where_clause = ""

    # Agregar filtros de estados si existen
    if estados:
        if where_clause:
            where_clause += " AND"
        else:
            where_clause += " WHERE"
        where_clause += " e.\"estado\" IN :estados"
        params['estados'] = tuple(estados)
    
    # Agregar filtros de tipos si existen
    if tipos:
        if 'WHERE' not in where_clause:
            where_clause += " WHERE"
        else:
            where_clause += " AND"
        where_clause += " m.\"siglas\" IN :tipos"
        params['tipos'] = tuple(tipos)

    # Obtener el total con todos los filtros aplicados
    total = get_total(where_clause, params)

    # Construir el título basado en los filtros aplicados
    if dist:
        title = f'Número de Defensorías en {dist}, {prov}, {dpto}: {total}'
    elif prov:
        title = f'Número de Defensorías por Distrito en {prov}, {dpto}: {total}'
    elif dpto:
        title = f'Número de Defensorías por Provincia en {dpto}: {total}'
    else:
        title = f'Número de Defensorías por Departamento: {total}'

    # Completar la consulta principal
    query += " e.\"estado\", m.\"siglas\", COUNT(*) as count FROM dna d JOIN estadodna e ON d.estado_acreditacion = e.codigo JOIN modelodna m ON d.modelo = m.codigo" + where_clause
    query += " GROUP BY ubicacion, e.\"estado\", m.\"siglas\""

    # Ejecutar la consulta
    df = run_query(query, params)

    # Gráfico de defensorías por ubicación
    fig_ubicacion = px.bar(df.groupby('ubicacion').sum().reset_index(), 
                        x='ubicacion', y='count',
                        title=title,
                        labels={'ubicacion': 'Ubicación', 'count': 'Número de Defensorías'},
                        color_discrete_sequence=colores_seaborn)

    # Gráfico de defensorías por estado de acreditación
    fig_estado = px.pie(df, values='count', names='estado', 
                        title=f'Distribución de Defensorías por Estado de Acreditación',
                        color_discrete_sequence=colores_seaborn)

    # Gráfico de defensorías por tipo de defensoría
    fig_tipo = px.pie(df, values='count', names='siglas', 
                    title=f'Distribución de Defensorías por Tipo de Defensoría',
                    color_discrete_sequence=colores_seaborn)

    # Personalización adicional para mejorar la apariencia
    for fig in [fig_ubicacion, fig_estado, fig_tipo]:
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family="Arial", size=12),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
    # Para el gráfico de barras, añadimos algunas personalizaciones específicas
    fig_ubicacion.update_xaxes(tickangle=-45)
    fig_ubicacion.update_yaxes(gridcolor='lightgray')

    return fig_ubicacion, fig_estado, fig_tipo

@app.callback(
    Output('acreditacion-por-fechas', 'figure'),
    [Input('fecha-inicio', 'date'),
     Input('fecha-fin', 'date'),
     Input('dpto-dna-dropdown', 'value'),
     Input('prov-dna-dropdown', 'value'),
     Input('dist-dna-dropdown', 'value'),
     Input('estado-dna-dropdown', 'value'),
     Input('tipo-dna-dropdown', 'value')]
)
def update_timeline(fecha_inicio, fecha_fin, dpto, prov, dist, estados, tipos):
    # Construir la consulta SQL base
    query = """
    SELECT d.f_acreditacion, COUNT(*) as count
    FROM dna d
    JOIN estadodna e ON d.estado_acreditacion = e.codigo
    JOIN modelodna m ON d.modelo = m.codigo
    WHERE d.f_acreditacion BETWEEN :fecha_inicio AND :fecha_fin
    """
    params = {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin}
    
    # Agregar filtros de ubicación
    if dist:
        query += " AND d.dpto = :dpto AND d.prov = :prov AND d.dist = :dist"
        params.update({'dpto': dpto, 'prov': prov, 'dist': dist})
    elif prov:
        query += " AND d.dpto = :dpto AND d.prov = :prov"
        params.update({'dpto': dpto, 'prov': prov})
    elif dpto:
        query += " AND d.dpto = :dpto"
        params.update({'dpto': dpto})
    
    # Agregar filtros de estados si existen
    if estados:
        query += " AND e.estado IN :estados"
        params['estados'] = tuple(estados)
    
    # Agregar filtros de tipos si existen
    if tipos:
        query += " AND m.siglas IN :tipos"
        params['tipos'] = tuple(tipos)
    
    # Agrupar por fecha de acreditación
    query += " GROUP BY d.f_acreditacion ORDER BY d.f_acreditacion"
    
    # Ejecutar la consulta
    df = run_query(query, params)
    
    # Convertir la columna de fecha a datetime
    df['f_acreditacion'] = pd.to_datetime(df['f_acreditacion'])
    
    # Ordenar el DataFrame por fecha
    df = df.sort_values('f_acreditacion')
    
    # Calcular la frecuencia acumulada
    df['cumulative_count'] = df['count'].cumsum()
    
    # Asegurar que tenemos una fila para cada día en el rango de fechas
    date_range = pd.date_range(start=fecha_inicio, end=fecha_fin)
    df_full = pd.DataFrame({'f_acreditacion': date_range})
    df = pd.merge(df_full, df, on='f_acreditacion', how='left')
    df['cumulative_count'] = df['cumulative_count'].ffill().fillna(0)
    
    # Crear el gráfico de línea con frecuencia acumulada
    fig = px.line(df, x='f_acreditacion', y='cumulative_count', 
                  title='Número Acumulado de Defensorías Acreditadas por Fecha',
                  labels={'f_acreditacion': 'Fecha de Acreditación', 'cumulative_count': 'Número Acumulado de Defensorías'})

    # Actualizar el trazo de la línea
    fig.update_traces(line=dict(color=colores_seaborn[0], width=2))
    
    # Personalizar el diseño del gráfico
    fig.update_layout(
        xaxis_title='Fecha de Acreditación',
        yaxis_title='Número Acumulado de Defensorías',
        hovermode='x unified',
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            tickformat='%Y-%m-%d'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray'
        ),
        title=dict(font=dict(size=16))
    )

    # Personalizar el formato de la información sobre la marcha (hover)
    fig.update_traces(
        hovertemplate='<b>Fecha</b>: %{x|%Y-%m-%d}<br><b>Total Acumulado</b>: %{y}<extra></extra>'
    )
    
    return fig




def format_date(date_string):
    if pd.notnull(date_string):
        return pd.to_datetime(date_string).strftime('%d/%m/%Y')
    return ''

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
        m.siglas AS "Tipo de DNA",
        d.dpto AS "Departamento",
        d.prov AS "Provincia",
        d.dist AS "Distrito",
        e.estado AS "Estado de Acreditación",
        d.f_acreditacion AS "Fecha de Acreditación",
        d.resolución_acreditación AS "Resolución de Acreditación",
        d.direccion AS "Dirección DNA",
        d.fono1 AS "Teléfono DNA",
        d.email AS "Correo electrónico DNA",
        d.horario AS "Horario de atención",
        d.f_inicio AS "Fecha Resolución de Creación",
        d.doc_creacion AS "Resolución de Creación",
        d.f_rof AS "Fecha Resolución de ROF",
        d.rof AS "Resolución de ROF",
        d.estado_registro AS "Estado de Registro",
        d.f_registro AS "Fecha de Registro",
        d.resolución_inscripción AS "Resolución de Inscripción",
        d.def_f AS "Defensoras",
        d.def_m AS "Defensores",
        d.promdef_f AS "Promotoras",
        d.promdef_m AS "Promotores",
        d.otros_f AS "Otras",
        d.otros_m AS "Otros",
        d.f_supervisión AS "Última fecha de supervisión",
        d.observaciones AS "Observaciones de la supervisión",
        d.curso AS "Último curso",
        d.f_curso AS "Fecha del último curso",
        d.f_cconna AS "Fecha CCONNA",
        d.fortalecida AS "DNA Fortalecida"
    FROM dna d
    JOIN modelodna m ON d.modelo = m.codigo
    JOIN estadodna e ON d.estado_acreditacion = e.codigo
    WHERE d.codigo = :codigo
    """
    
    df = run_query(query, {'codigo': codigo})
    
    if df.empty:
        return html.Div("No se encontraron resultados para esta DNA."), None
    
    # Formatear fechas
    date_columns = ['Fecha de Acreditación', 'Fecha Resolución de Creación', 'Fecha Resolución de ROF', 
                    'Fecha de Registro', 'Última fecha de supervisión', 'Fecha del último curso', 'Fecha CCONNA']
    for col in date_columns:
        df[col] = df[col].apply(format_date)
    
    # Calcular totales de personal
    total_mujeres = df['Defensoras'].fillna(0).iloc[0] + df['Promotoras'].fillna(0).iloc[0] + df['Otras'].fillna(0).iloc[0]
    total_hombres = df['Defensores'].fillna(0).iloc[0] + df['Promotores'].fillna(0).iloc[0] + df['Otros'].fillna(0).iloc[0]
    
    # Estilos para la tabla
    table_style = {
        'border-collapse': 'separate',
        'border-spacing': '0',
        'width': '100%',
        'font-family': 'Arial, sans-serif',
        'border': '1px solid #ddd',
        'border-radius': '8px',
        'overflow': 'hidden',
        'box-shadow': '0 0 20px rgba(0, 0, 0, 0.1)'
    }
    
    th_style = {
        'background-color': '#f8f8f8',
        'color': '#333',
        'font-weight': 'bold',
        'padding': '12px',
        'text-align': 'left',
        'border-bottom': '2px solid #ddd'
    }
    
    td_style = {
        'padding': '12px',  
        'text-align': 'left',
        'border-bottom': '1px solid #ddd'
    }
    
    # Crear tabla HTML personalizada
    table = html.Table([
        html.Thead(
            html.Tr([html.Th('Información General', colSpan=4, style=th_style), 
                     html.Th('Detalles de Acreditación', colSpan=4, style=th_style)])
        ),
        html.Tbody([
            html.Tr([
                html.Td('Tipo de DNA:', style=td_style), html.Td(df['Tipo de DNA'].iloc[0], style=td_style),
                html.Td('Departamento:', style=td_style), html.Td(df['Departamento'].iloc[0], style=td_style),
                html.Td('Estado de Acreditación:', style=td_style), html.Td(df['Estado de Acreditación'].iloc[0], style=td_style),
                html.Td('Fecha de Acreditación:', style=td_style), html.Td(df['Fecha de Acreditación'].iloc[0], style=td_style)
            ]),
            html.Tr([
                html.Td('Provincia:', style=td_style), html.Td(df['Provincia'].iloc[0], style=td_style),
                html.Td('Distrito:', style=td_style), html.Td(df['Distrito'].iloc[0], style=td_style),
                html.Td('Resolución de Acreditación:', style=td_style), html.Td(df['Resolución de Acreditación'].iloc[0], style=td_style),
                html.Td('Estado de Registro:', style=td_style), html.Td(df['Estado de Registro'].iloc[0], style=td_style)
            ]),
            html.Tr([html.Th('Información de Contacto', colSpan=4, style=th_style), 
                     html.Th('Información Legal', colSpan=4, style=th_style)]),
            html.Tr([
                html.Td('Dirección DNA:', style=td_style), html.Td(df['Dirección DNA'].iloc[0], style=td_style),
                html.Td('Teléfono DNA:', style=td_style), html.Td(df['Teléfono DNA'].iloc[0], style=td_style),
                html.Td('Fecha Resolución de Creación:', style=td_style), html.Td(df['Fecha Resolución de Creación'].iloc[0], style=td_style),
                html.Td('Resolución de Creación:', style=td_style), html.Td(df['Resolución de Creación'].iloc[0], style=td_style)
            ]),
            html.Tr([
                html.Td('Correo electrónico DNA:', style=td_style), html.Td(df['Correo electrónico DNA'].iloc[0], style=td_style),
                html.Td('Horario de atención:', style=td_style), html.Td(df['Horario de atención'].iloc[0], style=td_style),
                html.Td('Fecha Resolución de ROF:', style=td_style), html.Td(df['Fecha Resolución de ROF'].iloc[0], style=td_style),
                html.Td('Resolución de ROF:', style=td_style), html.Td(df['Resolución de ROF'].iloc[0], style=td_style)
            ]),
            html.Tr([html.Th('Personal', colSpan=4, style=th_style), 
                     html.Th('Información Adicional', colSpan=4, style=th_style)]),
            html.Tr([
                html.Td('Defensoras:', style=td_style), html.Td(df['Defensoras'].iloc[0], style=td_style),
                html.Td('Defensores:', style=td_style), html.Td(df['Defensores'].iloc[0], style=td_style),
                html.Td('Última fecha de supervisión:', style=td_style), html.Td(df['Última fecha de supervisión'].iloc[0], style=td_style),
                html.Td('Observaciones de la supervisión:', style=td_style), html.Td(df['Observaciones de la supervisión'].iloc[0], style=td_style)
            ]),
            html.Tr([
                html.Td('Promotoras:', style=td_style), html.Td(df['Promotoras'].iloc[0], style=td_style),
                html.Td('Promotores:', style=td_style), html.Td(df['Promotores'].iloc[0], style=td_style),
                html.Td('Último curso:', style=td_style), html.Td(df['Último curso'].iloc[0], style=td_style),
                html.Td('Fecha del último curso:', style=td_style), html.Td(df['Fecha del último curso'].iloc[0], style=td_style)
            ]),
            html.Tr([
                html.Td('Otras:', style=td_style), html.Td(df['Otras'].iloc[0], style=td_style),
                html.Td('Otros:', style=td_style), html.Td(df['Otros'].iloc[0], style=td_style),
                html.Td('Fecha CCONNA:', style=td_style), html.Td(df['Fecha CCONNA'].iloc[0], style=td_style),
                html.Td('DNA Fortalecida:', style=td_style), html.Td(df['DNA Fortalecida'].iloc[0], style=td_style)
            ]),
            html.Tr([
                html.Td('Total Mujeres:', style=td_style), html.Td(total_mujeres, style=td_style),
                html.Td('Total Hombres:', style=td_style), html.Td(total_hombres, style=td_style),
                html.Td(style=td_style), html.Td(style=td_style),
                html.Td(style=td_style), html.Td(style=td_style)
            ])
        ])
    ], style=table_style)
    
    return html.Div([
        html.H3(f"Resultados para DNA {codigo}"),
        table
    ]), None