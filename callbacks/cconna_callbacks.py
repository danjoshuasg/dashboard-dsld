from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
from datetime import datetime
import math

colores_seaborn = px.colors.qualitative.Set2

'''
dpto-cconna-dropdown: Departamentos
prov-cconna-dropdown: Provincias
dist-cconna-dropdown: Distritos
tipo-cconna-dropdown: Tipos de CCONNA
creacion-cconna-dropdown: Estado de creación de CCONNA
vigencia-cconna-dropdown: Estado de vigencia de CCONNA
'''

# Código para cargar los departamentos
@app.callback(
    Output('dpto-cconna-dropdown', 'options'),
    Input('dpto-cconna-dropdown', 'search_value')
)
def load_dptos(search_value):
    query = 'SELECT DISTINCT "dpto" FROM dna ORDER BY "dpto"'
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['dpto']]

# Código para cargar las provincias según el departamento seleccionado
@app.callback(
    Output('prov-cconna-dropdown', 'options'),
    Input('dpto-cconna-dropdown', 'value')
)
def set_provincias_options(selected_dpto):
    if selected_dpto:
        query = 'SELECT DISTINCT "prov" FROM dna WHERE "dpto" = :dpto ORDER BY "prov"'
        df = run_query(query, {'dpto': selected_dpto})
        return [{'label': i, 'value': i} for i in df['prov']]
    return []

# Código para cargar los distritos según la provincia seleccionada
@app.callback(
    Output('dist-cconna-dropdown', 'options'),
    Input('prov-cconna-dropdown', 'value'),
    State('dpto-cconna-dropdown', 'value')
)
def set_distritos_options(selected_prov, selected_dpto):
    if selected_prov and selected_dpto:
        query = 'SELECT DISTINCT "dist" FROM dna WHERE "dpto" = :dpto AND "prov" = :prov ORDER BY "dist"'
        df = run_query(query, {'dpto': selected_dpto, 'prov': selected_prov})
        return [{'label': i, 'value': i} for i in df['dist']]
    return []

# Callback para cargar los tipos de CCONNA
@app.callback(
    Output('tipo-cconna-dropdown', 'options'),
    Input('tipo-cconna-dropdown', 'search_value')
)
def load_tipo_cconna(search_value):
    query = 'SELECT DISTINCT "Tipo de CCONNA " AS tipo_cconna FROM cconna ORDER BY "Tipo de CCONNA "'
    df = run_query(query)
    return [{'label': i, 'value': i} for i in df['tipo_cconna']]

# Callback para el dropdown de creación del CCONNA
@app.callback(
    Output('creacion-cconna-dropdown', 'options'),
    Input('creacion-cconna-dropdown', 'search_value')
)
def load_creacion_cconna(search_value):
    query = """
        SELECT DISTINCT 
            CASE 
                WHEN "Fecha de la Ordenanza" IS NOT NULL THEN 'Creada' 
                ELSE 'No creada' 
            END AS estado_creacion
        FROM cconna
        ORDER BY estado_creacion
    """
    df = run_query(query)
    estados = df['estado_creacion'].unique()
    options = [{'label': estado, 'value': estado} for estado in estados]
    return options

# Callback para el dropdown de vigencia del CCONNA
@app.callback(
    Output('vigencia-cconna-dropdown', 'options'),
    Input('creacion-cconna-dropdown', 'value')
)
def set_vigencia_cconna(creacion_selected):
    if creacion_selected == 'Creada':
        query = """
            SELECT "Fecha de inicio del CCONNA", "Fecha de termino del CCONNA"
            FROM cconna
            WHERE "Fecha de la Ordenanza" IS NOT NULL
        """
        df = run_query(query)

        def parse_date(date_str):
            if pd.isnull(date_str) or date_str.strip() == '':
                return pd.NaT
            for fmt in ('%d/%m/%Y', '%Y', '%Y-%m-%d', '%d-%m-%Y'):
                try:
                    return pd.to_datetime(date_str, format=fmt, dayfirst=True)
                except (ValueError, TypeError):
                    continue
            return pd.to_datetime(date_str, errors='coerce')

        df['fecha_inicio'] = df['Fecha de inicio del CCONNA'].apply(parse_date)
        df['fecha_termino'] = df['Fecha de termino del CCONNA'].apply(parse_date)

        today = pd.to_datetime(datetime.today().date())

        def determine_vigencia(row):
            if pd.isnull(row['fecha_inicio']):
                return 'No Vigente'
            elif pd.isnull(row['fecha_termino']):
                if row['fecha_inicio'] <= today:
                    return 'Vigente'
                else:
                    return 'No Vigente'
            else:
                if row['fecha_inicio'] <= today <= row['fecha_termino']:
                    return 'Vigente'
                else:
                    return 'No Vigente'

        df['estado_vigencia'] = df.apply(determine_vigencia, axis=1)

        # Asegurarse de que ambas opciones aparezcan en el dropdown
        options = [{'label': 'Vigente', 'value': 'Vigente'},
                   {'label': 'No Vigente', 'value': 'No Vigente'}]
        return options
    else:
        return []
