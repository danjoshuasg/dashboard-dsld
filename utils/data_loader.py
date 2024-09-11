import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde la variable de entorno
db_url = os.getenv('postgresql_dsld_url')

# Crear la conexión a PostgreSQL
engine = create_engine(db_url)

# Función para ejecutar consultas SQL
def run_query(query, params=None):
    with engine.connect() as connection:
        result = connection.execute(text(query), params)
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    
def load_defensorias_data():
    try:

        # Leer los datos de la tabla dna
        df = pd.read_sql_table('dna', engine)
        
        # Cerrar la conexión
        engine.dispose()
        
        return df
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error


def load_capacitaciones_data():
    try:
        # Leer los datos de la tabla dna
        df = pd.read_sql_table('capacitaciones', engine)
        
        # Cerrar la conexión
        engine.dispose()
        
        return df
    except Exception as e:
        print(f"Error al cargar los datos: {e}")
        return pd.DataFrame()  # Devolver un DataFrame vacío en caso de error

