import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

# Cargar variables de entorno
load_dotenv()

# Obtener la URL de la base de datos desde la variable de entorno
db_url = os.getenv('postgresql_dsld_url')

# Crear la conexión a PostgreSQL
engine = create_engine(db_url)

# Función para ejecutar consultas SQL
def run_query(query, params=None):
    try:
        with engine.begin() as connection:  # Usa engine.begin() para manejar transacciones automáticamente
            result = connection.execute(text(query), params)
            if result.returns_rows:
                # Si la consulta devuelve filas (por ejemplo, SELECT), retornarlas como DataFrame
                return pd.DataFrame(result.fetchall(), columns=result.keys())
            else:
                # Para consultas que no devuelven filas (UPDATE, INSERT, DELETE), simplemente retornar None
                return None
    except SQLAlchemyError as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

def actualizar_ubigeo():
    # Verificar si ya existe 'Áncash' en la tabla
    verificar_existencia_query = "SELECT COUNT(*) AS count FROM ubigeo WHERE nombre = 'Áncash';"
    resultado = run_query(verificar_existencia_query)

    if resultado is not None and resultado['count'][0] == 0:
        # Si no existe 'Áncash', realizar la actualización
        update_query = "UPDATE ubigeo SET nombre = 'Áncash' WHERE nombre = 'Ancash';"
        run_query(update_query)
        print("Actualización realizada exitosamente.")
    else:
        print("La actualización ya se ha realizado previamente o 'Áncash' ya existe.")

    # (Opcional) Confirmar que la actualización se realizó correctamente
    verificar_query = "SELECT * FROM ubigeo WHERE nombre = 'Áncash';"
    df = run_query(verificar_query)
    print("Registros actualizados:")
    print(df)

if __name__ == "__main__":
    actualizar_ubigeo()
    # Aquí puedes llamar a otras funciones de carga de datos si es necesario
