"""Herramientas de limpieza para el dataset integrado.

Este módulo procesa CSVs en chunks para manejar archivos grandes, normaliza
los nombres de columnas, recorta espacios en strings, elimina duplicados y
filas completamente vacías, e intenta parsear columnas de fecha si su nombre
contiene 'date'.

Uso:
	python -m Extract.Clean.Clean --input <ruta_csv> --output <ruta_salida>

La salida será un CSV escrito por chunks en `output`.
"""

from __future__ import annotations

import argparse
import os
from typing import Optional

import pandas as pd


def normalize_column_name(name: str) -> str:
	# Normaliza nombres: strip, lower, reemplaza espacios por guiones bajos
	return name.strip().lower().replace(" ", "_").replace("\n", "_")


def clean_chunk(df: pd.DataFrame) -> pd.DataFrame:
	# Normalizar nombres de columnas una sola vez fuera de la función
	# Limpiar strings: strip y convertir cadenas vacías a NaN
	for col in df.select_dtypes(include=[object]).columns:
		df[col] = df[col].astype(str).map(lambda s: s.strip() if s is not None else s)
		df[col] = df[col].replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

	# Intentar parsear columnas que parezcan fechas
	for col in df.columns:
		if "date" in col.lower():
			try:
				df[col] = pd.to_datetime(df[col], errors="coerce")
			except Exception:
				# si falla, dejamos los valores tal como están
				pass

	return df


def clean_csv(input_path: str, output_path: str, chunk_size: int = 100_000, overwrite: bool = True) -> None:
	"""Limpia un CSV por chunks y escribe el resultado en output_path.

	- Normaliza nombres de columnas
	- Recorta strings y convierte cadenas vacías a NaN
	- Intenta parsear columnas de fecha
	- Elimina filas duplicadas (por chunk y luego globalmente)
	- Elimina filas completamente vacías
	"""
	if not os.path.exists(os.path.dirname(output_path)):
		os.makedirs(os.path.dirname(output_path), exist_ok=True)

	first_chunk = True
	seen_hashes = set()

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

