from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
import math

colores_seaborn = px.colors.qualitative.Set2

# Callback para actualizar los dropdowns de ubicación
@app.callback(
    [Output('region-cconna-dropdown', 'options'),
     Output('provincia-cconna-dropdown', 'options'),
     Output('distrito-cconna-dropdown', 'options')],
    [Input('region-cconna-dropdown', 'value'),
     Input('provincia-cconna-dropdown', 'value')]
)
def update_location_dropdowns(region, provincia):
    query = 'SELECT DISTINCT "Región", "Provincia", "Distrito" FROM cconna'
    df = run_query(query)
    
    regiones = [{'label': r, 'value': r} for r in sorted(df['Región'].unique())]
    
    if region:
        provincias = [{'label': p, 'value': p} for p in sorted(df[df['Región'] == region]['Provincia'].unique())]
    else:
        provincias = []
    
    if provincia:
        distritos = [{'label': d, 'value': d} for d in sorted(df[(df['Región'] == region) & (df['Provincia'] == provincia)]['Distrito'].unique())]
    else:
        distritos = []
    
    return regiones, provincias, distritos

# Callback para actualizar los dropdowns de tipo y estado
@app.callback(
    [Output('tipo-cconna-dropdown', 'options'),
     Output('estado-cconna-dropdown', 'options')],
    [Input('region-cconna-dropdown', 'value'),
     Input('provincia-cconna-dropdown', 'value'),
     Input('distrito-cconna-dropdown', 'value')]
)
def update_type_state_dropdowns(region, provincia, distrito):
    query = 'SELECT DISTINCT "Tipo de CCONNA ", "ESTADO" FROM cconna'
    conditions = []
    params = {}
    if region:
        conditions.append('"Región" = :region')
        params['region'] = region
    if provincia:
        conditions.append('"Provincia" = :provincia')
        params['provincia'] = provincia
    if distrito:
        conditions.append('"Distrito" = :distrito')
        params['distrito'] = distrito
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    df = run_query(query, params)
    
    tipos = [{'label': t, 'value': t} for t in sorted(df['Tipo de CCONNA '].unique())]
    estados = [{'label': e, 'value': e} for e in sorted(df['ESTADO'].unique())]
    
    return tipos, estados

# Callback para actualizar los gráficos
@app.callback(
    [Output('cconna-por-region', 'figure'),
     Output('cconna-por-tipo', 'figure'),
     Output('cconna-por-estado', 'figure'),
     Output('cconna-timeline', 'figure')],
    [Input('region-cconna-dropdown', 'value'),
     Input('provincia-cconna-dropdown', 'value'),
     Input('distrito-cconna-dropdown', 'value'),
     Input('tipo-cconna-dropdown', 'value'),
     Input('estado-cconna-dropdown', 'value')]
)
def update_graphs(region, provincia, distrito, tipo, estado):
    query = 'SELECT * FROM cconna'
    conditions = []
    params = {}
    if region:
        conditions.append('"Región" = :region')
        params['region'] = region
    if provincia:
        conditions.append('"Provincia" = :provincia')
        params['provincia'] = provincia
    if distrito:
        conditions.append('"Distrito" = :distrito')
        params['distrito'] = distrito
    if tipo:
        conditions.append('"Tipo de CCONNA " = :tipo')
        params['tipo'] = tipo
    if estado:
        conditions.append('"ESTADO" = :estado')
        params['estado'] = estado
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    df = run_query(query, params)
    
    # Gráfico por región
    region_counts = df['Región'].value_counts().reset_index()
    region_counts.columns = ['Región', 'Cantidad']
    fig_region = px.bar(region_counts, x='Región', y='Cantidad', 
                        title='CCONNAs por Región',
                        color_discrete_sequence=colores_seaborn)
    
    # Gráfico por tipo
    fig_tipo = px.pie(df, names='Tipo de CCONNA ', title='Distribución por Tipo de CCONNA',
                      color_discrete_sequence=colores_seaborn)
    
    # Gráfico por estado
    fig_estado = px.pie(df, names='ESTADO', title='Distribución por Estado',
                        color_discrete_sequence=colores_seaborn)
    
    # Timeline
    def parse_date(date_str):
        if pd.isna(date_str):
            return pd.NaT
        try:
            return pd.to_datetime(date_str, format='%Y')
        except ValueError:
            try:
                return pd.to_datetime(date_str, format='%Y-%m-%d')
            except ValueError:
                try:
                    return pd.to_datetime(date_str, format='%d/%m/%Y')
                except ValueError:
                    return pd.NaT

    df['Fecha de inicio del CCONNA'] = df['Fecha de inicio del CCONNA'].apply(parse_date)
    
    # Filtrar fechas válidas
    df_timeline = df[df['Fecha de inicio del CCONNA'].notna()]
    
    fig_timeline = px.scatter(df_timeline, x='Fecha de inicio del CCONNA', y='Región', 
                              title='Timeline de Creación de CCONNAs',
                              labels={'Fecha de inicio del CCONNA': 'Fecha de Inicio'},
                              color='Tipo de CCONNA ', color_discrete_sequence=colores_seaborn)
    
    return fig_region, fig_tipo, fig_estado, fig_timeline

# Callback para actualizar la tabla de datos
@app.callback(
    Output('tabla-cconna', 'data'),
    [Input('region-cconna-dropdown', 'value'),
     Input('provincia-cconna-dropdown', 'value'),
     Input('distrito-cconna-dropdown', 'value'),
     Input('tipo-cconna-dropdown', 'value'),
     Input('estado-cconna-dropdown', 'value'),
     Input('tabla-cconna', 'page_current'),
     Input('tabla-cconna', 'page_size')]
)
def update_table(region, provincia, distrito, tipo, estado, page_current, page_size):
    query = "SELECT * FROM cconna"
    conditions = []
    params = {}
    if region:
        conditions.append("Región = :region")
        params['region'] = region
    if provincia:
        conditions.append("Provincia = :provincia")
        params['provincia'] = provincia
    if distrito:
        conditions.append("Distrito = :distrito")
        params['distrito'] = distrito
    if tipo:
        conditions.append("`Tipo de CCONNA` = :tipo")
        params['tipo'] = tipo
    if estado:
        conditions.append("ESTADO = :estado")
        params['estado'] = estado
    
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    
    query += f" LIMIT {page_size} OFFSET {page_current * page_size}"
    
    df = run_query(query, params)
    
    return df.to_dict('records')

# Callback para la búsqueda de CCONNA específico
@app.callback(
    Output('cconna-results', 'children'),
    [Input('buscar-cconna-btn', 'n_clicks')],
    [State('cconna-input', 'value')]
)
def search_cconna(n_clicks, search_value):
    if n_clicks is None or not search_value:
        return html.Div()
    
    query = "SELECT * FROM cconna WHERE REGISTRO = :search_value OR `Nombre del CCONNA` LIKE :search_pattern"
    params = {'search_value': search_value, 'search_pattern': f'%{search_value}%'}
    df = run_query(query, params)
    
    if df.empty:
        return html.Div("No se encontraron resultados.", className='text-danger')
    
    result = df.iloc[0]
    return html.Div([
        html.H3(f"CCONNA: {result['Nombre del CCONNA']}"),
        html.P(f"Registro: {result['REGISTRO']}"),
        html.P(f"Ubicación: {result['Región']}, {result['Provincia']}, {result['Distrito']}"),
        html.P(f"Tipo de CCONNA: {result['Tipo de CCONNA']}"),
        html.P(f"Fecha de inicio: {result['Fecha de inicio del CCONNA']}"),
        html.P(f"Fecha de término: {result['Fecha de termino del CCONNA']}"),
        html.P(f"Estado: {result['ESTADO']}"),
        html.P(f"Área encargada: {result['Área encargada (Gerencia, Jefatura, Oficina o servicio) del CC']}"),
        html.P(f"Especialista encargado: {result['Nombres del Especialista encargado del CCONNA']} {result['Apellidos del Especialista encargado del CCONNA']}"),
        html.P(f"Contacto del especialista: {result['Correo Electrónico del Especialista encargado del CCONNA']}, Tel: {result['Teléfono del Especialista encargado del CCONNA']}")
    ])