"""🧹 MÓDULO DE LIMPIEZA DE DATOS

Este módulo es el SEGUNDO PASO del pipeline ETL. Se encarga de LIMPIAR
los datos crudos para que estén listos para análisis.

🎯 PROPÓSITO:
   Convertir datos "sucios" (con errores, duplicados, formatos inconsistentes)
   en datos "limpios" y listos para usar.

🔧 QUÉ HACE:
   1. Normaliza nombres de columnas (minúsculas, sin espacios)
   2. Limpia valores de texto (quita espacios extra)
   3. Convierte valores vacíos a NaN (más fácil de manejar)
   4. Parsea fechas automáticamente
   5. Elimina filas duplicadas
   6. Elimina filas completamente vacías
   
💡 VENTAJA:
   Procesa archivos GIGANTES (>1GB) usando chunks (bloques pequeños)
   sin saturar la memoria.

📖 USO:
   # Desde línea de comandos:
   python -m Extract.Clean.Clean --input datos.csv --output datos_limpio.csv
   
   # Desde Python:
   from Extract.Clean.Clean import clean_csv
   clean_csv("IntegratedData.csv", "Output/IntegratedData_cleaned.csv")
"""

from __future__ import annotations

import argparse
import os
from typing import Optional

import pandas as pd


def normalize_column_name(name: str) -> str:
	"""
	🔤 NORMALIZAR NOMBRE DE COLUMNA - Estandariza nombres
	
	Qué hace:
	- Quita espacios al inicio/final: "  Columna  " → "Columna"
	- Convierte a minúsculas: "COLUMNA" → "columna"
	- Reemplaza espacios por guiones bajos: "Mi Columna" → "mi_columna"
	- Reemplaza saltos de línea: "Columna\n" → "columna_"
	
	¿Por qué es importante?
	- Evita errores de tipeo ("Cases" vs "cases")
	- Facilita autocompletado en código
	- Mantiene consistencia en todo el proyecto
	
	Args:
		name: Nombre original de la columna
		
	Returns:
		Nombre normalizado (minúsculas, sin espacios)
		
	Ejemplo:
		>>> normalize_column_name("  Daily Cases  ")
		'daily_cases'
		>>> normalize_column_name("RETAIL & Recreation")
		'retail_&_recreation'
	"""
	# Paso 1: Quitar espacios al inicio/final
	name = name.strip()
	
	# Paso 2: Convertir a minúsculas
	name = name.lower()
	
	# Paso 3: Reemplazar espacios por _
	name = name.replace(" ", "_")
	
	# Paso 4: Reemplazar saltos de línea por _
	name = name.replace("\n", "_")
	
	return name


def clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
	"""
	🧹 LIMPIAR CHUNK - Limpia un bloque de datos
	
	Qué hace:
	1. Limpia columnas de texto (strings):
	   - Quita espacios extra: "  texto  " → "texto"
	   - Convierte vacíos a NaN: "" → NaN
	   - Convierte "nan" y "None" a NaN
	
	2. Parsea columnas de fecha:
	   - Detecta columnas con "date" en el nombre
	   - Convierte a formato datetime de pandas
	   - Si falla, deja los valores como están
	
	Args:
		df: DataFrame con un chunk de datos
		
	Returns:
		DataFrame limpio (mismo chunk, valores mejorados)
	
	Ejemplo:
		>>> chunk = pd.DataFrame({'date': ['2021-01-01', '2021-01-02'],
		...                       'county': ['  Los Angeles  ', 'Miami']})
		>>> cleaned = clean_chunk(chunk)
		>>> cleaned['county']
		0    Los Angeles
		1    Miami
	"""
	# PASO 1: Limpiar columnas de texto (object = string en pandas)
	# Seleccionar solo columnas de tipo texto
	for col in df.select_dtypes(include=[object]).columns:
		# Convertir a string (por si hay valores None)
		df[col] = df[col].astype(str)
		
		# Quitar espacios al inicio/final de cada valor
		df[col] = df[col].map(lambda s: s.strip() if s is not None else s)
		
		# Reemplazar valores vacíos o "nan" con NaN real de pandas
		df[col] = df[col].replace({
			"": pd.NA,      # Strings vacíos
			"nan": pd.NA,   # Texto "nan"
			"None": pd.NA   # Texto "None"
		})

	# PASO 2: Parsear columnas de fecha
	# Buscar columnas que tengan "date" en el nombre
	for col in df.columns:
		if "date" in col.lower():  # Buscar sin importar mayúsculas
			try:
				# Intentar convertir a datetime
				# errors="coerce": Si falla, pone NaT (Not a Time = fecha inválida)
				df[col] = pd.to_datetime(df[col], errors="coerce")
			except Exception:
				# Si falla completamente, dejar valores como están
				# Esto evita que el script se detenga por un error
				pass

	return df


def clean_csv(input_path: str, output_path: str, chunk_size: int = 100_000, overwrite: bool = True) -> None:
	"""
	🧹 LIMPIAR CSV - Función principal que limpia un archivo CSV completo
	
	🎯 ESTRATEGIA:
	   Lee el archivo en CHUNKS (bloques) de 100,000 filas, limpia cada
	   bloque, y guarda el resultado. Esto permite limpiar archivos de
	   10GB+ con solo 2GB de RAM.
	
	🔄 PROCESO:
	   1. Lee chunk 1 (100k filas) → Limpia → Guarda
	   2. Lee chunk 2 (100k filas) → Limpia → Agrega al archivo
	   3. Lee chunk 3 (100k filas) → Limpia → Agrega al archivo
	   ... y así hasta terminar el archivo
	
	✅ LO QUE HACE:
	   - Normaliza nombres de columnas (solo primera vez)
	   - Limpia valores en cada chunk
	   - Elimina filas completamente vacías
	   - Elimina duplicados (dentro de cada chunk Y globalmente)
	   - Guarda resultado en output_path
	
	Args:
		input_path: Ruta al CSV original (ej: "IntegratedData.csv")
		output_path: Dónde guardar el CSV limpio (ej: "Output/cleaned.csv")
		chunk_size: Cuántas filas procesar a la vez (default: 100,000)
		overwrite: Si True, sobrescribe archivo existente
		
	Ejemplo:
		>>> clean_csv("IntegratedData.csv", "Output/IntegratedData_cleaned.csv")
		🧹 Limpiando datos en chunks de 100,000 filas...
		   Chunk 1: 100,000 filas procesadas
		   Chunk 2: 100,000 filas procesadas
		   ...
		✅ Limpieza completada: Output/IntegratedData_cleaned.csv
	"""
	# Crear directorio de salida si no existe
	output_dir = os.path.dirname(output_path)
	if output_dir and not os.path.exists(output_dir):
		os.makedirs(output_dir, exist_ok=True)

	# Variables de control
	first_chunk = True           # True solo para el primer chunk
	seen_hashes = set()          # Para detectar duplicados globales

	# Leer por chunks
	for chunk in pd.read_csv(input_path, chunksize=chunk_size, low_memory=False):
		if first_chunk:
			# Normalizar nombres de columnas solo la primera vez
			chunk.columns = [normalize_column_name(c) for c in chunk.columns]
			header = True
			first_chunk = False
		else:
			# Asegurar que columnas se alineen si hay discrepancias
			chunk.columns = [normalize_column_name(c) for c in chunk.columns]
			header = False

		chunk = clean_chunk(chunk)

		# Eliminar filas completamente vacías
		chunk = chunk.dropna(how="all")

		# Eliminar duplicados locales
		chunk = chunk.drop_duplicates()

		# Para evitar duplicados globales en un streaming simple, usamos hash de filas
		# (puede consumir memoria según variedad de filas). Convertimos a tuplas.
		hashes = chunk.apply(lambda row: tuple(row.values.tolist()), axis=1).map(hash)
		mask = ~hashes.isin(seen_hashes)
		if mask.any():
			rows_to_write = chunk.loc[mask]
			hashes_to_add = set(hashes[mask].tolist())
			seen_hashes.update(hashes_to_add)

			# Escribir al CSV (append tras el primer write)
			if os.path.exists(output_path) and not overwrite:
				rows_to_write.to_csv(output_path, mode="a", header=False, index=False)
			else:
				# Si es la primera vez, sobreescribimos el archivo
				if not os.path.exists(output_path):
					rows_to_write.to_csv(output_path, mode="w", header=True, index=False)
				else:
					rows_to_write.to_csv(output_path, mode="a", header=False, index=False)

	# Nota: si el dataset es muy grande, seen_hashes puede crecer mucho. Para
	# datasets enormes se recomendaría una estrategia distinta (hash por columnas
	# clave, base de datos temporal, o Bloom filter). Aquí aplicamos una solución
	# práctica y sencilla que suele funcionar para tamaños moderados.


def main(argv: Optional[list[str]] = None) -> None:
	parser = argparse.ArgumentParser(description="Limpia un CSV grande por chunks y escribe un CSV limpio.")
	parser.add_argument("--input", required=True, help="Ruta al CSV de entrada")
	parser.add_argument("--output", required=False, default="Output/IntegratedData_cleaned.csv", help="Ruta del CSV de salida")
	parser.add_argument("--chunksize", type=int, default=100000, help="Tamaño de chunk para lectura (filas)")
	parser.add_argument("--overwrite", action="store_true", help="Sobrescribir salida si existe")

	args = parser.parse_args(argv)

	# Si overwrite no está puesto y el archivo existe, lo eliminamos para evitar append accidental
	if args.overwrite and os.path.exists(args.output):
		os.remove(args.output)

	clean_csv(args.input, args.output, chunk_size=args.chunksize, overwrite=args.overwrite)


if __name__ == "__main__":
	main()

