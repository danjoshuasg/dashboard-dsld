from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
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

# Callbacks para estados de DNA corregido
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

@app.callback(
    [Output('dna-por-ubicacion', 'figure'),
     Output('dna-por-estado', 'figure')],
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
    
    if dist:
        query += " d.\"dist\" as ubicacion,"
        where_clause = " WHERE d.\"dpto\" = :dpto AND d.\"prov\" = :prov AND d.\"dist\" = :dist"
        params = {'dpto': dpto, 'prov': prov, 'dist': dist}
        title = f'Número de Defensorías en {dist}, {prov}, {dpto}'
    elif prov:
        query += " d.\"dist\" as ubicacion,"
        where_clause = " WHERE d.\"dpto\" = :dpto AND d.\"prov\" = :prov"
        params = {'dpto': dpto, 'prov': prov}
        title = f'Número de Defensorías por Distrito en {prov}, {dpto}'
    elif dpto:
        query += " d.\"prov\" as ubicacion,"
        where_clause = " WHERE d.\"dpto\" = :dpto"
        params = {'dpto': dpto}
        title = f'Número de Defensorías por Provincia en {dpto}'
    else:
        query += " d.\"dpto\" as ubicacion,"
        where_clause = ""
        title = 'Número de Defensorías por Departamento'

    # Construir la parte de la consulta con los JOINs y el WHERE
    query += " e.\"estado\", m.\"siglas\", COUNT(*) as count FROM dna d JOIN estadodna e ON d.estado_acreditacion = e.codigo JOIN modelodna m ON d.modelo = m.codigo" + where_clause

    # Agregar filtros de estados si existen
    if estados:
        if where_clause:
            query += " AND"
        else:
            query += " WHERE"
        query += " e.\"estado\" IN :estados"
        params['estados'] = tuple(estados)
    
    # Agregar filtros de tipos si existen
    if tipos:
        if 'WHERE' not in query:
            query += " WHERE"
        else:
            query += " AND"
        query += " m.\"siglas\" IN :tipos"
        params['tipos'] = tuple(tipos)

    # Completar la consulta con el GROUP BY
    query += " GROUP BY ubicacion, e.\"estado\", m.\"siglas\""

    # Ejecutar la consulta
    df = run_query(query, params)

    # Gráfico de defensorías por ubicación
    fig_ubicacion = px.bar(df.groupby('ubicacion').sum().reset_index(), 
                           x='ubicacion', y='count',
                           title=title,
                           labels={'ubicacion': 'Ubicación', 'count': 'Número de Defensorías'})
    
    # Gráfico de defensorías por estado de acreditación
    fig_estado = px.pie(df, values='count', names='estado', 
                        title='Distribución de Defensorías por Estado de Acreditación')

    return fig_ubicacion, fig_estado




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