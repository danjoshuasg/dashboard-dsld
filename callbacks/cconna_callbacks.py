from dash import Input, Output, State, dash_table, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from app import app  # Importar la instancia de la aplicación desde app.py
from utils.data_loader import run_query
from datetime import datetime
import unicodedata
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
    query = '''
    SELECT "ubigeo", "nombre"
    FROM ubigeo
    WHERE "ubigeo" LIKE '__0000' AND "ubigeo" != '000000'
    ORDER BY "nombre"
    '''
    df = run_query(query)
    
    # Modificar 'Lima' a 'Lima Metropolitana' y agregar 'Lima Provincia'
    options = []
    for index, row in df.iterrows():
        if row['nombre'] == 'Lima':
            # Agregar 'Lima Metropolitana'
            options.append({'label': 'Lima Metropolitana', 'value': '150000'})  # Usar '150000' como código
            # Agregar 'Lima Provincia' con un código personalizado
            options.append({'label': 'Lima Provincia', 'value': '260000'})  # Usar '260000' como código
        else:
            options.append({'label': row['nombre'], 'value': row['ubigeo']})
    return options

# Código para cargar las provincias según el departamento seleccionado
@app.callback(
    Output('prov-cconna-dropdown', 'options'),
    Input('dpto-cconna-dropdown', 'value')
)
def set_provincias_options(selected_dpto_code):
    if selected_dpto_code:
        if selected_dpto_code == '150000':  # Lima Metropolitana
            # Cargar solo la provincia de Lima
            query = '''
            SELECT "ubigeo", "nombre"
            FROM ubigeo
            WHERE "ubigeo" = '150100'
            ORDER BY "nombre"
            '''
            df = run_query(query)
        elif selected_dpto_code == '260000':  # Lima Provincia
            # Cargar todas las provincias de Lima excepto la provincia de Lima (código '150100')
            query = '''
            SELECT "ubigeo", "nombre"
            FROM ubigeo
            WHERE "ubigeo" LIKE '15__00' AND "ubigeo" NOT IN ('150000', '150100')
            ORDER BY "nombre"
            '''
            df = run_query(query)
        else:
            dpto_code = selected_dpto_code[:2]
            query = '''
            SELECT "ubigeo", "nombre"
            FROM ubigeo
            WHERE "ubigeo" LIKE :dpto_code || '__00' AND "ubigeo" NOT LIKE :dpto_code || '0000'
            ORDER BY "nombre"
            '''
            params = {'dpto_code': dpto_code}
            df = run_query(query, params)
        options = [{'label': row['nombre'], 'value': row['ubigeo']} for index, row in df.iterrows()]
        return options
    return []


# Código para cargar los distritos según la provincia seleccionada
@app.callback(
    Output('dist-cconna-dropdown', 'options'),
    Input('prov-cconna-dropdown', 'value')
)
def set_distritos_options(selected_prov_code):
    if selected_prov_code:
        dpto_prov_code = selected_prov_code[:4]
        query = '''
        SELECT "ubigeo", "nombre"
        FROM ubigeo
        WHERE "ubigeo" LIKE :dpto_prov_code || '__' AND "ubigeo" NOT LIKE :dpto_prov_code || '00'
        ORDER BY "nombre"
        '''
        params = {'dpto_prov_code': dpto_prov_code}
        df = run_query(query, params)
        options = [{'label': row['nombre'], 'value': row['ubigeo']} for index, row in df.iterrows()]
        return options
    return []


# Callback para cargar los tipos de CCONNA
@app.callback(
    Output('tipo-cconna-dropdown', 'options'),
    [Input('dpto-cconna-dropdown', 'value'),
     Input('prov-cconna-dropdown', 'value'),
     Input('dist-cconna-dropdown', 'value')]
)
def load_tipo_cconna(selected_dpto_code, selected_prov_code, selected_dist_code):
    # Función para obtener el nombre a partir del código UBIGEO
    def get_nombre_from_ubigeo(ubigeo_code):
        if not ubigeo_code:
            return None
        if ubigeo_code == '150000':
            return 'Lima Metropolitana'
        elif ubigeo_code == '260000':
            return 'Lima Provincia'
        else:
            query = 'SELECT "nombre" FROM ubigeo WHERE "ubigeo" = :ubigeo_code'
            df = run_query(query, {'ubigeo_code': ubigeo_code})
            if not df.empty:
                return df.iloc[0]['nombre']
            else:
                return None

    # Obtener los nombres correspondientes a los códigos UBIGEO seleccionados
    dpto_nombre = get_nombre_from_ubigeo(selected_dpto_code)
    prov_nombre = get_nombre_from_ubigeo(selected_prov_code)
    dist_nombre = get_nombre_from_ubigeo(selected_dist_code)

    # Definir los tipos de CCONNA disponibles
    all_types = ['CCONNA Regional', 'CCONNA Provincial', 'CCONNA Distrital']

    # Caso 1: No se ha seleccionado ni departamento, provincia ni distrito
    if not selected_dpto_code and not selected_prov_code and not selected_dist_code:
        # Se pueden seleccionar tipos Regional, Provincial y Distrital
        query = '''
            SELECT DISTINCT "Tipo de CCONNA " AS tipo_cconna
            FROM cconna
            WHERE "Tipo de CCONNA " IN ('CCONNA Regional', 'CCONNA Provincial', 'CCONNA Distrital')
            ORDER BY "Tipo de CCONNA "
        '''
        df = run_query(query)

    # Caso 2: Se ha seleccionado departamento pero no provincia ni distrito
    elif selected_dpto_code and not selected_prov_code and not selected_dist_code:
        # Se pueden seleccionar tipos Provincial y Distrital
        query = '''
            SELECT DISTINCT "Tipo de CCONNA " AS tipo_cconna
            FROM cconna
            WHERE "Tipo de CCONNA " IN ('CCONNA Provincial', 'CCONNA Distrital')
            AND "Región" = :dpto
            ORDER BY "Tipo de CCONNA "
        '''
        df = run_query(query, {'dpto': dpto_nombre})

    # Caso 3: Se ha seleccionado provincia pero no distrito
    elif selected_prov_code and not selected_dist_code:
        # Solo se puede seleccionar tipo Distrital
        query = '''
            SELECT DISTINCT "Tipo de CCONNA " AS tipo_cconna
            FROM cconna
            WHERE "Tipo de CCONNA " = 'CCONNA Distrital'
            AND "Región" = :dpto
            AND "Provincia" = :prov
            ORDER BY "Tipo de CCONNA "
        '''
        df = run_query(query, {'dpto': dpto_nombre, 'prov': prov_nombre})

    # Caso 4: Se ha seleccionado distrito
    elif selected_dist_code:
        # Solo se puede seleccionar tipo Distrital (si aplica)
        query = '''
            SELECT DISTINCT "Tipo de CCONNA " AS tipo_cconna
            FROM cconna
            WHERE "Tipo de CCONNA " = 'CCONNA Distrital'
            AND "Región" = :dpto
            AND "Provincia" = :prov
            AND "Distrito" = :dist
            ORDER BY "Tipo de CCONNA "
        '''
        df = run_query(query, {'dpto': dpto_nombre, 'prov': prov_nombre, 'dist': dist_nombre})
    else:
        # No se muestran opciones
        return []

    # Crear la lista de opciones para el dropdown
    if not df.empty:
        options = [{'label': tipo.strip(), 'value': tipo.strip()} for tipo in df['tipo_cconna']]
    else:
        options = []

    return options

# Callback para el dropdown de creación del CCONNA
@app.callback(
    Output('creacion-cconna-dropdown', 'options'),
    Input('creacion-cconna-dropdown', 'search_value')
)
def load_creacion_cconna(search_value):
    query = """
        SELECT 
            CASE 
                WHEN COALESCE(
                    "¿Cuenta con Acta de Conformación o Acta de Elección? SI/NO",
                    "¿Cuenta con Ordenanza que crea el CCONNA? SI/NO",
                    "¿Cuenta con Resolución de conformación de integrantes del CC"
                ) IS NOT NULL THEN 'Creada' 
                ELSE 'No creada' 
            END AS estado_creacion
        FROM cconna
        GROUP BY estado_creacion
        ORDER BY estado_creacion
    """
    df = run_query(query)
    estados = df['estado_creacion'].unique()
    options = [{'label': estado, 'value': estado} for estado in estados]
    return options


# Callback para el dropdown de documento del CCONNA
@app.callback(
    Output('documento-cconna-dropdown', 'options'),
    Input('documento-cconna-dropdown', 'search_value')
)
def load_documento_cconna(search_value):
    query = """
        SELECT DISTINCT
            CASE
                WHEN "¿Cuenta con Acta de Conformación o Acta de Elección? SI/NO" IS NOT NULL THEN 'Acta de Conformación/Elección'
                WHEN "¿Cuenta con Ordenanza que crea el CCONNA? SI/NO" IS NOT NULL THEN 'Ordenanza de creación'
                WHEN "¿Cuenta con Resolución de conformación de integrantes del CC" IS NOT NULL THEN 'Resolución de Conformación'
                ELSE 'Sin Documento'
            END AS tipo_documento
        FROM cconna
        WHERE "¿Cuenta con Acta de Conformación o Acta de Elección? SI/NO" IS NOT NULL
           OR "¿Cuenta con Ordenanza que crea el CCONNA? SI/NO" IS NOT NULL
           OR "¿Cuenta con Resolución de conformación de integrantes del CC" IS NOT NULL
        ORDER BY tipo_documento
    """
    df = run_query(query)
    documentos = df['tipo_documento'].unique()
    options = [{'label': doc, 'value': doc} for doc in documentos]
    return options


# Callback para el dropdown de vigencia del CCONNA
@app.callback(
    Output('vigencia-cconna-dropdown', 'options'),
    Input('creacion-cconna-dropdown', 'value')
)
def set_vigencia_cconna(creacion_selected):
    if creacion_selected == ['Creada']:
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
        vigencias = df['estado_vigencia'].unique()

        # Asegurarse de que ambas opciones aparezcan en el dropdown
        options = [{'label': vigencia, 'value': vigencia} for vigencia in vigencias]
    else:
        options = []
    return options



@app.callback(
    [Output('cconna-por-ubicacion', 'figure'),        
     Output('cconna-por-tipo', 'figure'),
     Output('cconna-por-creacion', 'figure'),
     Output('cconna-por-vigencia', 'figure')],
    [Input('dpto-cconna-dropdown', 'value'),
     Input('prov-cconna-dropdown', 'value'),
     Input('dist-cconna-dropdown', 'value'),
     Input('tipo-cconna-dropdown', 'value'),
     Input('creacion-cconna-dropdown', 'value'),
     Input('vigencia-cconna-dropdown', 'value')]
)
def update_graphs(dpto_code, prov_code, dist_code, tipo, creacion, vigencia):
    # Función para obtener el nombre a partir del código UBIGEO
    def get_nombre_from_ubigeo(ubigeo_code):
        if not ubigeo_code:
            return None
        if ubigeo_code == '150000':
            return 'Lima Metropolitana'
        elif ubigeo_code == '260000':
            return 'Lima Provincia'
        else:
            query = 'SELECT "nombre" FROM ubigeo WHERE "ubigeo" = :ubigeo_code'
            df = run_query(query, {'ubigeo_code': ubigeo_code})
            if not df.empty:
                return df.iloc[0]['nombre']
            else:
                return None

    # Obtener los nombres correspondientes a los códigos UBIGEO seleccionados
    dpto_nombre = get_nombre_from_ubigeo(dpto_code)
    prov_nombre = get_nombre_from_ubigeo(prov_code)
    dist_nombre = get_nombre_from_ubigeo(dist_code)
    
    # Construir la consulta SQL base
    query = "SELECT * FROM cconna WHERE 1=1"
    params = {}

    # Filtrar por departamento
    if dpto_nombre:
        query += ' AND "Región" = :dpto'
        params['dpto'] = dpto_nombre

    # Filtrar por provincia
    if prov_nombre:
        query += ' AND "Provincia" = :prov'
        params['prov'] = prov_nombre

    # Filtrar por distrito
    if dist_nombre:
        query += ' AND "Distrito" = :dist'
        params['dist'] = dist_nombre

    # Filtrar por tipo de CCONNA
    if tipo:
        if isinstance(tipo, list):
            query += ' AND "Tipo de CCONNA " IN :tipo'
            params['tipo'] = tuple(tipo)
        else:
            query += ' AND "Tipo de CCONNA " = :tipo'
            params['tipo'] = tipo

    # Filtrar por estado de creación
    if creacion:
        if isinstance(creacion, list):
            creacion_conditions = []
            for estado in creacion:
                if estado == 'Creada':
                    creacion_conditions.append('"Fecha de la Ordenanza" IS NOT NULL')
                elif estado == 'No creada':
                    creacion_conditions.append('"Fecha de la Ordenanza" IS NULL')
            query += ' AND (' + ' OR '.join(creacion_conditions) + ')'
        else:
            if creacion == 'Creada':
                query += ' AND "Fecha de la Ordenanza" IS NOT NULL'
            elif creacion == 'No creada':
                query += ' AND "Fecha de la Ordenanza" IS NULL'

    # Ejecutar la consulta
    df = run_query(query, params)

    # Procesar el estado de vigencia
    def parse_date(date_str):
        if pd.isnull(date_str) or str(date_str).strip() == '':
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

    # Filtrar por estado de vigencia
    if vigencia:
        if isinstance(vigencia, list):
            df = df[df['estado_vigencia'].isin(vigencia)]
        else:
            df = df[df['estado_vigencia'] == vigencia]

    # Verificar si el DataFrame está vacío
    if df.empty:
        # Crear figuras vacías con un mensaje
        fig_ubicacion = px.bar(title='No hay datos disponibles para la ubicación seleccionada.')
        fig_tipo = px.pie(title='No hay datos disponibles para el tipo seleccionado.')
        fig_creacion = px.pie(title='No hay datos disponibles para el estado de creación seleccionado.')
        fig_vigencia = px.pie(title='No hay datos disponibles para el estado de vigencia seleccionado.')
        return fig_ubicacion, fig_tipo, fig_creacion, fig_vigencia

    # Figura 1: Histograma según la ubicación
    if dist_nombre:
        ubicacion_field = 'Distrito'
    elif prov_nombre:
        ubicacion_field = 'Distrito'  # Mostrar a nivel de distrito si se selecciona provincia
    elif dpto_nombre:
        ubicacion_field = 'Provincia'  # Mostrar a nivel de provincia si se selecciona departamento
    else:
        ubicacion_field = 'Región'

    count_df = df[ubicacion_field].value_counts().reset_index()
    count_df.columns = [ubicacion_field, 'Cantidad']
    fig_ubicacion = px.bar(count_df, x=ubicacion_field, y='Cantidad', title=f'CCONNA por {ubicacion_field}')

    # Figura 2: Pie chart según el tipo de CCONNA
    tipo_counts = df['Tipo de CCONNA '].value_counts().reset_index()
    tipo_counts.columns = ['Tipo de CCONNA', 'Cantidad']
    fig_tipo = px.pie(tipo_counts, names='Tipo de CCONNA', values='Cantidad', title='Distribución por Tipo de CCONNA')

    # Figura 3: Pie chart según el estado de creación
    df['estado_creacion'] = df['Fecha de la Ordenanza'].apply(lambda x: 'Creada' if pd.notnull(x) else 'No creada')
    creacion_counts = df['estado_creacion'].value_counts().reset_index()
    creacion_counts.columns = ['Estado de Creación', 'Cantidad']
    fig_creacion = px.pie(creacion_counts, names='Estado de Creación', values='Cantidad', title='Distribución por Estado de Creación')

    # Figura 4: Pie chart según el estado de vigencia
    vigencia_counts = df['estado_vigencia'].value_counts().reset_index()
    vigencia_counts.columns = ['Estado de Vigencia', 'Cantidad']
    fig_vigencia = px.pie(vigencia_counts, names='Estado de Vigencia', values='Cantidad', title='Distribución por Estado de Vigencia')

    return fig_ubicacion, fig_tipo, fig_creacion, fig_vigencia