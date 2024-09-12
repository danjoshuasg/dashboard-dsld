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
