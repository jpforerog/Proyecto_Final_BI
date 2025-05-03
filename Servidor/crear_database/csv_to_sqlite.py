import pandas as pd
import sqlite3

# Configuración
CSV_FILE = "df_procesado_final.csv"  # Ruta de tu archivo CSV
DB_NAME = "partidos.db"  # Nombre de la base de datos SQLite
TABLE_NAME = "PARTIDOS"  # Nombre de la tabla a crear

df = pd.read_csv(CSV_FILE, dtype=str)


def convertir_columna(columna, tipo):
    try:
        if tipo == 'Int64':
            return pd.to_numeric(columna, errors='coerce').round().astype('Int64')
        elif tipo == 'float64':
            return pd.to_numeric(columna, errors='coerce').astype('float64')
        elif tipo == 'boolean':
            return columna.str.strip('*') == 'Sí'
        elif tipo == 'datetime64':
            return pd.to_datetime(columna, errors='coerce')
        else:
            return columna.astype(tipo)
    except Exception as e:
        print(f"Error convirtiendo columna: {str(e)}")
        return columna

# Mapeo de tipos para columnas críticas
conversion_map = {
    'Succ': 'Int64',          # Columna 46 - Entero nullable
    'Gls_90': 'Int64',        # Columna 47
    'victoria_penales': 'Int64',
    'derrota_penales': 'Int64',
    'Arranque': 'boolean',    # Convertir a booleano
    'Fecha': 'datetime64',
    'Rendimiento': 'float64',
    'Rendimiento_normalizado': 'float64'
}

# Aplicar conversiones
for col, tipo in conversion_map.items():
    df[col] = convertir_columna(df[col], tipo)

# --------------------------------------------------
# Paso 3: Guardar en SQLite
# --------------------------------------------------
try:
    conn = sqlite3.connect(DB_NAME)
    
    # Tipos explícitos para SQLite
    dtype_sql = {
        'Fecha': 'DATETIME',
        'Arranque': 'BOOLEAN',
        'Succ': 'INTEGER',
        'Gls_90': 'INTEGER'
    }
    
    df.to_sql(
        name=TABLE_NAME,
        con=conn,
        if_exists='replace',
        index=False,
        dtype=dtype_sql
    )
    print(f"✅ ¡Base de datos {DB_NAME} creada exitosamente!")

except Exception as e:
    print(f"🚨 Error fatal: {str(e)}")
    
finally:
    if 'conn' in locals():
        conn.close()