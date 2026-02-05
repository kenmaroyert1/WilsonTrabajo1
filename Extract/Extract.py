"""📥 MÓDULO DE EXTRACCIÓN DE DATOS

Este módulo es el PRIMER PASO del pipeline ETL. Se encarga de LEER datos
desde archivos CSV grandes de manera eficiente.

🎯 PROPÓSITO:
   Cargar datos de IntegratedData.csv (77MB) en memoria de forma inteligente,
   con múltiples estrategias según necesidades (todo, chunks, muestra, filtrado).

🔧 QUÉ HACE:
   - Lee archivos CSV grandes sin saturar la memoria
   - Valida que el archivo exista y sea legible
   - Ofrece 7 métodos diferentes de extracción
   - Filtra por estados, fechas, o columnas específicas
   - Procesa por chunks para archivos gigantes

💡 CÓMO USAR:
   ```python
   from Extract.Extract import DataExtractor
   
   # Crear extractor
   extractor = DataExtractor("IntegratedData.csv")
   
   # Opción 1: Cargar todo
   df = extractor.extract_full()
   
   # Opción 2: Solo California
   df = extractor.extract_by_state(['California'])
   
   # Opción 3: Procesar por chunks (archivos muy grandes)
   for chunk in extractor.extract_chunks(50000):
       process(chunk)
   ```
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, List, Iterator

import pandas as pd

# ============================================================================
# IMPORTAR CONFIGURACIONES
# ============================================================================
# Intenta importar configuración centralizada; si falla, usa valores por defecto

try:
    # Importar desde Config.py (lo ideal)
    from Config.Config import (
        RAW_DATA_FILE,      # Ruta al CSV original
        CHUNK_SIZE,         # Cuántas filas leer a la vez
        EXPECTED_COLUMNS,   # Qué columnas esperamos encontrar
        DATE_COLUMNS,       # Columnas de fecha (para parseo especial)
        NUMERIC_COLUMNS,    # Columnas numéricas
        CATEGORICAL_COLUMNS # Columnas de texto
    )
except ImportError:
    # Si Config.py no existe, usar valores por defecto
    RAW_DATA_FILE = Path("IntegratedData.csv")
    CHUNK_SIZE = 100_000
    EXPECTED_COLUMNS = None
    DATE_COLUMNS = ['date']
    NUMERIC_COLUMNS = []
    CATEGORICAL_COLUMNS = ['county', 'state']


# ============================================================================
# CLASE PRINCIPAL: DataExtractor
# ============================================================================

class DataExtractor:
    """
    🔧 EXTRACTOR DE DATOS - Lee archivos CSV de múltiples formas
    
    Esta clase ofrece 7 métodos diferentes para leer datos según tus necesidades:
    1. extract_full()         → Todo en memoria (si tienes RAM suficiente)
    2. extract_chunks()       → Por bloques (para archivos gigantes)
    3. extract_columns()      → Solo algunas columnas (ahorra memoria)
    4. extract_sample()       → Muestra aleatoria (para pruebas)
    5. extract_by_state()     → Filtrado por estados
    6. extract_date_range()   → Filtrado por fechas
    7. get_info()            → Info del archivo sin cargar datos
    """
    
    def __init__(self, file_path: str | Path = None, chunk_size: int = None):
        """
        🏗️ CONSTRUCTOR - Inicializa el extractor con la ruta del archivo
        
        Args:
            file_path: Ruta al archivo CSV (ej: "IntegratedData.csv")
                      Si no se proporciona, usa RAW_DATA_FILE de Config.py
            chunk_size: Cuántas filas leer a la vez (default: 100,000)
                       Más pequeño = menos memoria, más lento
                       Más grande = más memoria, más rápido
        
        Ejemplo:
            >>> extractor = DataExtractor("datos.csv", chunk_size=50000)
        """
        # Convertir ruta a Path si es string
        self.file_path = Path(file_path) if file_path else RAW_DATA_FILE
        
        # Guardar tamaño de chunk
        self.chunk_size = chunk_size or CHUNK_SIZE
        
        # Variables para almacenar metadatos (se llenan después)
        self.columns = None      # Nombres de columnas del CSV
        self.dtypes = None       # Tipos de datos de cada columna
        
    def validate_file(self) -> bool:
        """
        ✅ VALIDAR ARCHIVO - Verifica que el archivo exista y sea legible
        
        Qué hace:
        1. Verifica que el archivo existe en el disco
        2. Verifica que es un archivo (no un directorio)
        3. Calcula y muestra el tamaño en MB
        
        Returns:
            True si todo está bien
            
        Raises:
            FileNotFoundError: Si el archivo no existe
            ValueError: Si la ruta no es un archivo
        
        Ejemplo:
            >>> extractor = DataExtractor("datos.csv")
            >>> extractor.validate_file()
            📁 Archivo encontrado: datos.csv
            📊 Tamaño: 77.50 MB
        """
        # Paso 1: Verificar que existe
        if not self.file_path.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {self.file_path}")
        
        # Paso 2: Verificar que es un archivo (no directorio)
        if not self.file_path.is_file():
            raise ValueError(f"La ruta no es un archivo: {self.file_path}")
        
        # Paso 3: Calcular tamaño en MB
        size_bytes = self.file_path.stat().st_size        # Tamaño en bytes
        size_mb = size_bytes / (1024 * 1024)              # Convertir a MB
        
        # Mostrar información
        print(f"📁 Archivo encontrado: {self.file_path.name}")
        print(f"📊 Tamaño: {size_mb:.2f} MB")
        
        return True
    
    def extract_full(self, nrows: Optional[int] = None) -> pd.DataFrame:
        """
        📥 EXTRACCIÓN COMPLETA - Carga TODO el archivo en memoria
        
        🎯 CUÁNDO USAR:
           - Cuando tienes suficiente RAM (8GB+ para archivos de 77MB)
           - Cuando necesitas todos los datos a la vez
           - Para análisis que requieren el dataset completo
        
        ⚠️ ADVERTENCIA:
           - Archivos >1GB pueden saturar la memoria
           - Para archivos grandes, mejor usar extract_chunks()
        
        Args:
            nrows: Número máximo de filas a leer
                  None = leer todas las filas
                  100 = solo primeras 100 filas (útil para pruebas)
            
        Returns:
            pd.DataFrame con todos los datos cargados
        
        Ejemplo:
            >>> extractor = DataExtractor("IntegratedData.csv")
            >>> df = extractor.extract_full()
            🔄 Extrayendo datos desde IntegratedData.csv...
            ✅ Datos extraídos exitosamente
               - Filas: 935,444
               - Columnas: 17
        """
        # Validar que el archivo existe antes de leer
        self.validate_file()
        
        print(f"🔄 Extrayendo datos desde {self.file_path.name}...")
        
        try:
            # Leer CSV con pandas
            # low_memory=False: Lee todo de una vez (más RAM, más rápido)
            df = pd.read_csv(
                self.file_path,
                nrows=nrows,          # Limitar filas si se especifica
                low_memory=False      # Cargar todo en memoria
            )
            
            # Mostrar estadísticas de lo que se cargó
            print(f"✅ Datos extraídos exitosamente")
            print(f"   - Filas: {len(df):,}")              # :, agrega separadores de miles
            print(f"   - Columnas: {len(df.columns)}")
            
            # Guardar nombres de columnas para referencia futura
            self.columns = df.columns.tolist()
            
            return df
            
        except Exception as e:
            # Si algo sale mal, mostrar error y re-lanzar excepción
            print(f"❌ Error al extraer datos: {e}")
            raise
    
    def extract_chunks(self) -> Iterator[pd.DataFrame]:
        """
        📦 EXTRACCIÓN POR CHUNKS - Lee el archivo en bloques pequeños
        
        🎯 CUÁNDO USAR:
           - Archivos muy grandes (>1GB) que no caben en memoria
           - Cuando quieres procesar datos de a poco
           - Para streaming de datos sin cargar todo
        
        💡 VENTAJA:
           - Usa poca memoria (solo un chunk a la vez)
           - Puede procesar archivos de 10GB+ con solo 2GB RAM
        
        ⚠️ NOTA:
           - Es un GENERADOR (iterator), no retorna DataFrame directo
           - Debes iterar con un for loop
        
        Returns:
            Iterator que produce DataFrames de chunk_size filas cada uno
        
        Ejemplo:
            >>> extractor = DataExtractor("BigFile.csv", chunk_size=50000)
            >>> for chunk in extractor.extract_chunks():
            ...     # Procesar cada chunk
            ...     print(f"Procesando {len(chunk)} filas...")
            ...     process_data(chunk)
            📦 Leyendo en chunks de 50,000 filas...
            Procesando 50,000 filas...
            Procesando 50,000 filas...
            ...
        """
        
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
