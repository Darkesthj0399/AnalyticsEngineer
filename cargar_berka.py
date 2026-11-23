import duckdb
from pathlib import Path

# 1. CONEXIÓN: abre (o crea, si no existe) un archivo de base de datos
con = duckdb.connect("data/berka.duckdb")
carpeta = Path("data/raw")

for table in carpeta.glob("*.asc"):
# 2. CARGA: crea una tabla leyendo el archivo crudo
    nombre_tabla = table.stem
    if nombre_tabla == "order":
        nombre_tabla = "orders"
    con.execute(f"""
        CREATE OR REPLACE TABLE {nombre_tabla} AS
        SELECT *
        FROM read_csv('{table}', delim=';', header=true)
    """)

    # 3. VALIDACIÓN: consulta y trae el resultado a Python
    filas = con.execute(f"SELECT COUNT(*) FROM {nombre_tabla}").fetchone()[0]
    print(f"{nombre_tabla}:", filas)

# 4. CIERRE: libera el archivo
con.close()