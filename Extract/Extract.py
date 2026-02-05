"""Módulo de extracción de datos.

Este módulo maneja la lectura y carga inicial de datos desde archivos CSV.
Incluye funciones para lectura por chunks, validación de esquema y
extracción selectiva de datos.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List, Iterator

import pandas as pd

# Importar configuración si está disponible
try:
    from Config.Config import (
        RAW_DATA_FILE, CHUNK_SIZE, EXPECTED_COLUMNS,
        DATE_COLUMNS, NUMERIC_COLUMNS, CATEGORICAL_COLUMNS
    )
except ImportError:
    # Valores por defecto si no está disponible Config
    RAW_DATA_FILE = Path("IntegratedData.csv")
    CHUNK_SIZE = 100_000
    EXPECTED_COLUMNS = None
    DATE_COLUMNS = ['date']
    NUMERIC_COLUMNS = []
    CATEGORICAL_COLUMNS = ['county', 'state']


class DataExtractor:
    """Clase para extraer datos desde archivos CSV."""
    
    def __init__(self, file_path: str | Path = None, chunk_size: int = None):
        """
        Inicializa el extractor de datos.
        
        Args:
            file_path: Ruta al archivo CSV de entrada
            chunk_size: Tamaño de chunk para lectura por bloques
        """
        self.file_path = Path(file_path) if file_path else RAW_DATA_FILE
        self.chunk_size = chunk_size or CHUNK_SIZE
        self.columns = None
        self.dtypes = None
        
    def validate_file(self) -> bool:
        """Valida que el archivo exista y sea legible."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")
        
        if not self.file_path.is_file():
            raise ValueError(f"La ruta no es un archivo: {self.file_path}")
        
        # Verificar tamaño
        size_mb = self.file_path.stat().st_size / (1024 * 1024)
        print(f"📁 Archivo encontrado: {self.file_path.name}")
        print(f"📊 Tamaño: {size_mb:.2f} MB")
        
        return True
    
    def extract_full(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Extrae el dataset completo en memoria.
        
        Args:
            nrows: Número máximo de filas a leer (None = todas)
            
        Returns:
            DataFrame con los datos
        """
        self.validate_file()
        
        print(f"🔄 Extrayendo datos desde {self.file_path.name}...")
        
        try:
            df = pd.read_csv(
                self.file_path,
                nrows=nrows,
                low_memory=False
            )
            
            print(f"✅ Datos extraídos exitosamente")
            print(f"   - Filas: {len(df):,}")
            print(f"   - Columnas: {len(df.columns)}")
            
            self.columns = df.columns.tolist()
            return df
            
        except Exception as e:
            print(f"❌ Error al extraer datos: {e}")
            raise
    
    def extract_chunks(self) -> Iterator[pd.DataFrame]:
        """
        Extrae el dataset por chunks para procesamiento eficiente.
        
        Yields:
            DataFrames en chunks del tamaño especificado
        """
        self.validate_file()
        
        print(f"🔄 Extrayendo datos por chunks (tamaño: {self.chunk_size:,} filas)...")
        
        try:
            chunk_iterator = pd.read_csv(
                self.file_path,
                chunksize=self.chunk_size,
                low_memory=False
            )
            
            for i, chunk in enumerate(chunk_iterator, 1):
                print(f"   Chunk {i}: {len(chunk):,} filas", end='\r')
                yield chunk
            
            print()  # Nueva línea después de los chunks
            print(f"✅ Extracción por chunks completada")
            
        except Exception as e:
            print(f"\n❌ Error al extraer chunks: {e}")
            raise
    
    def extract_columns(self, columns: List[str], nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Extrae solo columnas específicas del dataset.
        
        Args:
            columns: Lista de nombres de columnas a extraer
            nrows: Número máximo de filas (None = todas)
            
        Returns:
            DataFrame con las columnas seleccionadas
        """
        self.validate_file()
        
        print(f"🔄 Extrayendo columnas específicas: {', '.join(columns)}")
        
        try:
            df = pd.read_csv(
                self.file_path,
                usecols=columns,
                nrows=nrows,
                low_memory=False
            )
            
            print(f"✅ Columnas extraídas exitosamente")
            return df
            
        except Exception as e:
            print(f"❌ Error al extraer columnas: {e}")
            raise
    
    def extract_sample(self, n: int = 1000, random: bool = True, seed: int = 42) -> pd.DataFrame:
        """
        Extrae una muestra del dataset.
        
        Args:
            n: Número de filas a extraer
            random: Si True, muestra aleatoria; si False, primeras n filas
            seed: Semilla para reproducibilidad (solo si random=True)
            
        Returns:
            DataFrame con la muestra
        """
        print(f"🔄 Extrayendo muestra ({'aleatoria' if random else 'secuencial'}) de {n:,} filas...")
        
        if random:
            # Primero obtener el total de filas
            df_full = self.extract_full()
            df_sample = df_full.sample(n=min(n, len(df_full)), random_state=seed)
        else:
            df_sample = self.extract_full(nrows=n)
        
        print(f"✅ Muestra extraída: {len(df_sample):,} filas")
        return df_sample
    
    def get_info(self) -> dict:
        """
        Obtiene información básica del archivo sin cargar todos los datos.
        
        Returns:
            Diccionario con información del archivo
        """
        self.validate_file()
        
        # Leer solo las primeras filas para obtener columnas
        df_head = pd.read_csv(self.file_path, nrows=5)
        
        # Contar líneas del archivo
        with open(self.file_path, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for _ in f) - 1  # -1 por el header
        
        return {
            'file_path': str(self.file_path),
            'file_size_mb': self.file_path.stat().st_size / (1024 * 1024),
            'total_rows': total_lines,
            'total_columns': len(df_head.columns),
            'columns': df_head.columns.tolist(),
            'dtypes': df_head.dtypes.to_dict()
        }
    
    def extract_by_state(self, state: str, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        Extrae datos filtrados por estado específico.
        
        Args:
            state: Nombre del estado a filtrar
            nrows: Límite de filas a procesar (None = todas)
            
        Returns:
            DataFrame filtrado por estado
        """
        print(f"🔄 Extrayendo datos para el estado: {state}")
        
        df = self.extract_full(nrows=nrows)
        df_filtered = df[df['state'].str.lower() == state.lower()].copy()
        
        print(f"✅ Datos extraídos: {len(df_filtered):,} filas para {state}")
        return df_filtered
    
    def extract_date_range(self, start_date: str, end_date: str) -> pd.DataFrame:
        """
        Extrae datos para un rango de fechas específico.
        
        Args:
            start_date: Fecha inicio (formato YYYY-MM-DD)
            end_date: Fecha fin (formato YYYY-MM-DD)
            
        Returns:
            DataFrame filtrado por rango de fechas
        """
        print(f"🔄 Extrayendo datos del {start_date} al {end_date}")
        
        df = self.extract_full()
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        df_filtered = df[mask].copy()
        
        print(f"✅ Datos extraídos: {len(df_filtered):,} filas")
        return df_filtered


def extract_data(file_path: Optional[str] = None, 
                 chunk_size: Optional[int] = None,
                 **kwargs) -> pd.DataFrame:
    """
    Función de conveniencia para extraer datos.
    
    Args:
        file_path: Ruta al archivo CSV
        chunk_size: Tamaño de chunk (no usado en extracción simple)
        **kwargs: Argumentos adicionales para pd.read_csv
        
    Returns:
        DataFrame con los datos extraídos
    """
    extractor = DataExtractor(file_path, chunk_size)
    return extractor.extract_full()


if __name__ == "__main__":
    # Ejemplo de uso
    print("="*60)
    print("MÓDULO DE EXTRACCIÓN DE DATOS")
    print("="*60)
    
    # Crear extractor
    extractor = DataExtractor()
    
    # Obtener información del archivo
    print("\n📋 Información del archivo:")
    try:
        info = extractor.get_info()
        for key, value in info.items():
            if key == 'columns':
                print(f"  {key}: {len(value)} columnas")
            elif key == 'dtypes':
                continue
            else:
                print(f"  {key}: {value}")
    except Exception as e:
        print(f"  ❌ No se pudo obtener información: {e}")
    
    # Extraer muestra
    print("\n📊 Extrayendo muestra de datos...")
    try:
        sample = extractor.extract_sample(n=100, random=True)
        print(f"\nPrimeras 3 filas de la muestra:")
        print(sample.head(3))
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    print("\n" + "="*60)
