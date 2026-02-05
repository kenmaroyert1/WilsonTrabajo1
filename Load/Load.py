"""💾 MÓDULO DE CARGA Y PERSISTENCIA DE DATOS

Este módulo es el CUARTO PASO del pipeline ETL. Se encarga de GUARDAR
los datos procesados en disco para uso posterior.

🎯 PROPÓSITO:
   Guardar datos transformados en múltiples formatos (CSV, Excel, JSON, Parquet)
   y facilitar su carga para análisis futuros o compartir con otros.

🔧 QUÉ HACE:
   1. Guarda datos en 4 formatos diferentes (CSV, Excel, JSON, Parquet)
   2. Crea backups automáticos con timestamp
   3. Guarda metadatos (info sobre los datos)
   4. Carga datos desde archivos guardados
   5. Lista y gestiona archivos de salida

💡 USO SIMPLE:
   ```python
   from Load.Load import DataLoader
   import pandas as pd
   
   # Crear loader
   loader = DataLoader()
   
   # Guardar en CSV
   df = pd.DataFrame({'A': [1,2,3], 'B': [4,5,6]})
   loader.save_to_csv(df, "resultados.csv")
   
   # Cargar de vuelta
   df_loaded = loader.load_from_csv("resultados.csv")
   
   # Crear backup
   loader.create_backup("resultados.csv")  # resultados_backup_20260204_103015.csv
   ```

📊 FORMATOS SOPORTADOS:
   - CSV: Universal, compatible con todo (Excel, R, Python)
   - Excel: Para reportes, análisis en Excel/Google Sheets
   - JSON: Para APIs, aplicaciones web
   - Parquet: Comprimido, 70% más pequeño que CSV, más rápido
"""

from __future__ import annotations

from typing import Optional, List
from pathlib import Path
import pandas as pd
import json
from datetime import datetime

# ============================================================================
# IMPORTAR CONFIGURACIONES
# ============================================================================

try:
    from Config.Config import OUTPUT_DIR, FIGURES_DIR, CHUNK_SIZE
except ImportError:
    OUTPUT_DIR = Path("Output")
    FIGURES_DIR = OUTPUT_DIR / "figures"
    CHUNK_SIZE = 100_000


# ============================================================================
# CLASE PRINCIPAL: DataLoader
# ============================================================================

class DataLoader:
    """
    💾 CARGADOR DE DATOS - Guarda y carga datos en múltiples formatos
    
    Esta clase facilita:
    - Guardar datos procesados (CSV, Excel, JSON, Parquet)
    - Cargar datos guardados
    - Crear backups con timestamp
    - Gestionar metadatos
    - Listar archivos de salida
    """
    
    def __init__(self, output_dir: Optional[Path] = None):
        """
        🏗️ CONSTRUCTOR - Inicializa el loader
        
        Args:
            output_dir: Dónde guardar archivos (default: Output/)
                       Si no existe, lo crea automáticamente
        
        Ejemplo:
            >>> loader = DataLoader()  # Usa Output/
            >>> loader = DataLoader("MisResultados/")  # Usa carpeta custom
        """
        # Usar OUTPUT_DIR de Config.py si no se especifica
        self.output_dir = Path(output_dir) if output_dir else OUTPUT_DIR
        
        # Crear directorio si no existe
        # parents=True: crea directorios padres también
        # exist_ok=True: no da error si ya existe
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def save_to_csv(self, 
                    df: pd.DataFrame, 
                    filename: str,
                    index: bool = False,
                    **kwargs) -> Path:
        """
        💾 GUARDAR CSV - Guarda DataFrame en formato CSV
        
        CSV = Comma Separated Values (valores separados por comas)
        - Formato universal, compatible con TODO
        - Fácil de abrir en Excel, Google Sheets, R, Python
        - Tamaño mediano (no comprimido)
        
        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo (ej: "resultados.csv")
                     Si no termina en .csv, se agrega automáticamente
            index: Si incluir índice del DataFrame (default: False)
            **kwargs: Argumentos extras para pandas.to_csv()
            
        Returns:
            Path: Ruta completa del archivo guardado
            
        Ejemplo:
            >>> loader = DataLoader()
            >>> df = pd.DataFrame({'A': [1,2,3]})
            >>> path = loader.save_to_csv(df, "datos.csv")
            ✅ CSV guardado: datos.csv (0.15 MB)
        Returns:
            Path del archivo guardado
        """
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = self.output_dir / filename
        df.to_csv(filepath, index=index, **kwargs)
        
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ CSV guardado: {filepath.name} ({size_mb:.2f} MB)")
        return filepath
    
    def save_to_csv_chunked(self,
                           df: pd.DataFrame,
                           filename: str,
                           chunk_size: int = None,
                           index: bool = False) -> Path:
        """
        Guarda DataFrame a CSV en chunks (para archivos grandes).
        
        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo
            chunk_size: Tamaño de chunk
            index: Si incluir índice
            
        Returns:
            Path del archivo guardado
        """
        chunk_size = chunk_size or CHUNK_SIZE
        
        if not filename.endswith('.csv'):
            filename += '.csv'
        
        filepath = self.output_dir / filename
        
        # Guardar en chunks
        for i, start in enumerate(range(0, len(df), chunk_size)):
            chunk = df.iloc[start:start + chunk_size]
            mode = 'w' if i == 0 else 'a'
            header = i == 0
            chunk.to_csv(filepath, mode=mode, header=header, index=index)
            print(f"  Chunk {i+1}: {len(chunk):,} filas guardadas")
        
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ CSV guardado (chunked): {filepath.name} ({size_mb:.2f} MB)")
        return filepath
    
    def save_to_excel(self,
                     df: pd.DataFrame,
                     filename: str,
                     sheet_name: str = 'Sheet1',
                     index: bool = False) -> Path:
        """
        Guarda DataFrame a archivo Excel.
        
        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo
            sheet_name: Nombre de la hoja
            index: Si incluir índice
            
        Returns:
            Path del archivo guardado
        """
        if not filename.endswith('.xlsx'):
            filename += '.xlsx'
        
        filepath = self.output_dir / filename
        df.to_excel(filepath, sheet_name=sheet_name, index=index)
        
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ Excel guardado: {filepath.name} ({size_mb:.2f} MB)")
        return filepath
    
    def save_to_json(self,
                    df: pd.DataFrame,
                    filename: str,
                    orient: str = 'records',
                    lines: bool = False) -> Path:
        """
        Guarda DataFrame a archivo JSON.
        
        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo
            orient: Formato JSON ('records', 'split', 'index', 'columns', 'values')
            lines: Si usar formato JSON Lines
            
        Returns:
            Path del archivo guardado
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.output_dir / filename
        df.to_json(filepath, orient=orient, lines=lines)
        
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ JSON guardado: {filepath.name} ({size_mb:.2f} MB)")
        return filepath
    
    def save_to_parquet(self,
                       df: pd.DataFrame,
                       filename: str,
                       compression: str = 'snappy') -> Path:
        """
        Guarda DataFrame a archivo Parquet.
        
        Args:
            df: DataFrame a guardar
            filename: Nombre del archivo
            compression: Tipo de compresión ('snappy', 'gzip', 'brotli')
            
        Returns:
            Path del archivo guardado
        """
        if not filename.endswith('.parquet'):
            filename += '.parquet'
        
        filepath = self.output_dir / filename
        df.to_parquet(filepath, compression=compression)
        
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"✅ Parquet guardado: {filepath.name} ({size_mb:.2f} MB)")
        return filepath
    
    def load_from_csv(self,
                     filename: str,
                     **kwargs) -> pd.DataFrame:
        """
        Carga DataFrame desde archivo CSV.
        
        Args:
            filename: Nombre del archivo
            **kwargs: Argumentos adicionales para read_csv
            
        Returns:
            DataFrame cargado
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        df = pd.read_csv(filepath, **kwargs)
        print(f"✅ CSV cargado: {filename} ({len(df):,} filas)")
        return df
    
    def load_from_excel(self,
                       filename: str,
                       sheet_name: str = 0,
                       **kwargs) -> pd.DataFrame:
        """
        Carga DataFrame desde archivo Excel.
        
        Args:
            filename: Nombre del archivo
            sheet_name: Nombre o índice de la hoja
            **kwargs: Argumentos adicionales para read_excel
            
        Returns:
            DataFrame cargado
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        df = pd.read_excel(filepath, sheet_name=sheet_name, **kwargs)
        print(f"✅ Excel cargado: {filename} ({len(df):,} filas)")
        return df
    
    def load_from_json(self,
                      filename: str,
                      orient: str = 'records',
                      lines: bool = False) -> pd.DataFrame:
        """
        Carga DataFrame desde archivo JSON.
        
        Args:
            filename: Nombre del archivo
            orient: Formato JSON
            lines: Si es formato JSON Lines
            
        Returns:
            DataFrame cargado
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        df = pd.read_json(filepath, orient=orient, lines=lines)
        print(f"✅ JSON cargado: {filename} ({len(df):,} filas)")
        return df
    
    def load_from_parquet(self, filename: str) -> pd.DataFrame:
        """
        Carga DataFrame desde archivo Parquet.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            DataFrame cargado
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        df = pd.read_parquet(filepath)
        print(f"✅ Parquet cargado: {filename} ({len(df):,} filas)")
        return df
    
    def create_backup(self, filename: str, backup_suffix: str = None) -> Path:
        """
        Crea copia de seguridad de un archivo.
        
        Args:
            filename: Nombre del archivo original
            backup_suffix: Sufijo para el backup (None = timestamp)
            
        Returns:
            Path del archivo de backup
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        if backup_suffix is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_suffix = f"backup_{timestamp}"
        
        # Obtener nombre y extensión
        stem = filepath.stem
        suffix = filepath.suffix
        backup_name = f"{stem}_{backup_suffix}{suffix}"
        backup_path = self.output_dir / backup_name
        
        # Copiar archivo
        import shutil
        shutil.copy2(filepath, backup_path)
        
        size_mb = backup_path.stat().st_size / (1024 * 1024)
        print(f"✅ Backup creado: {backup_name} ({size_mb:.2f} MB)")
        return backup_path
    
    def save_metadata(self,
                     filename: str,
                     metadata: dict,
                     json_filename: str = None) -> Path:
        """
        Guarda metadatos de un dataset.
        
        Args:
            filename: Nombre del archivo de datos
            metadata: Diccionario con metadatos
            json_filename: Nombre del archivo JSON (None = auto)
            
        Returns:
            Path del archivo de metadatos
        """
        if json_filename is None:
            stem = Path(filename).stem
            json_filename = f"{stem}_metadata.json"
        
        if not json_filename.endswith('.json'):
            json_filename += '.json'
        
        filepath = self.output_dir / json_filename
        
        # Agregar timestamp
        metadata['created_at'] = datetime.now().isoformat()
        metadata['source_file'] = filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Metadatos guardados: {json_filename}")
        return filepath
    
    def load_metadata(self, json_filename: str) -> dict:
        """
        Carga metadatos desde archivo JSON.
        
        Args:
            json_filename: Nombre del archivo de metadatos
            
        Returns:
            Diccionario con metadatos
        """
        filepath = self.output_dir / json_filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        print(f"✅ Metadatos cargados: {json_filename}")
        return metadata
    
    def list_files(self, extension: str = None) -> List[Path]:
        """
        Lista archivos en el directorio de salida.
        
        Args:
            extension: Filtrar por extensión (ej: '.csv')
            
        Returns:
            Lista de paths
        """
        if extension:
            if not extension.startswith('.'):
                extension = '.' + extension
            files = list(self.output_dir.glob(f"*{extension}"))
        else:
            files = [f for f in self.output_dir.iterdir() if f.is_file()]
        
        print(f"✅ {len(files)} archivos encontrados")
        return sorted(files)
    
    def get_file_info(self, filename: str) -> dict:
        """
        Obtiene información de un archivo.
        
        Args:
            filename: Nombre del archivo
            
        Returns:
            Diccionario con información del archivo
        """
        filepath = self.output_dir / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Archivo no encontrado: {filepath}")
        
        stat = filepath.stat()
        
        info = {
            'filename': filepath.name,
            'path': str(filepath),
            'size_bytes': stat.st_size,
            'size_mb': stat.st_size / (1024 * 1024),
            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
            'extension': filepath.suffix
        }
        
        print(f"📄 {filename}:")
        print(f"   Tamaño: {info['size_mb']:.2f} MB")
        print(f"   Modificado: {info['modified']}")
        
        return info


def save_data(df: pd.DataFrame,
             filename: str,
             format: str = 'csv',
             output_dir: Optional[Path] = None,
             **kwargs) -> Path:
    """
    Función de conveniencia para guardar datos en diferentes formatos.
    
    Args:
        df: DataFrame a guardar
        filename: Nombre del archivo
        format: Formato ('csv', 'excel', 'json', 'parquet')
        output_dir: Directorio de salida
        **kwargs: Argumentos adicionales
        
    Returns:
        Path del archivo guardado
    """
    loader = DataLoader(output_dir)
    
    format = format.lower()
    
    if format == 'csv':
        return loader.save_to_csv(df, filename, **kwargs)
    elif format in ['excel', 'xlsx']:
        return loader.save_to_excel(df, filename, **kwargs)
    elif format == 'json':
        return loader.save_to_json(df, filename, **kwargs)
    elif format == 'parquet':
        return loader.save_to_parquet(df, filename, **kwargs)
    else:
        raise ValueError(f"Formato no soportado: {format}")


def load_data(filename: str,
             format: str = None,
             output_dir: Optional[Path] = None,
             **kwargs) -> pd.DataFrame:
    """
    Función de conveniencia para cargar datos en diferentes formatos.
    
    Args:
        filename: Nombre del archivo
        format: Formato ('csv', 'excel', 'json', 'parquet'), None = detectar
        output_dir: Directorio de salida
        **kwargs: Argumentos adicionales
        
    Returns:
        DataFrame cargado
    """
    loader = DataLoader(output_dir)
    
    # Detectar formato por extensión si no se especifica
    if format is None:
        ext = Path(filename).suffix.lower()
        if ext == '.csv':
            format = 'csv'
        elif ext in ['.xlsx', '.xls']:
            format = 'excel'
        elif ext == '.json':
            format = 'json'
        elif ext == '.parquet':
            format = 'parquet'
        else:
            raise ValueError(f"No se pudo detectar formato para extensión: {ext}")
    
    format = format.lower()
    
    if format == 'csv':
        return loader.load_from_csv(filename, **kwargs)
    elif format in ['excel', 'xlsx']:
        return loader.load_from_excel(filename, **kwargs)
    elif format == 'json':
        return loader.load_from_json(filename, **kwargs)
    elif format == 'parquet':
        return loader.load_from_parquet(filename, **kwargs)
    else:
        raise ValueError(f"Formato no soportado: {format}")


if __name__ == "__main__":
    print("="*60)
    print("MÓDULO DE CARGA Y GUARDADO DE DATOS")
    print("="*60)
    
    # Ejemplo con datos sintéticos
    print("\n📊 Creando datos de ejemplo...")
    import numpy as np
    
    dates = pd.date_range('2021-01-01', periods=100)
    df_example = pd.DataFrame({
        'date': dates,
        'cases': np.random.randint(1000, 10000, 100),
        'deaths': np.random.randint(10, 100, 100)
    })
    
    # Crear loader
    loader = DataLoader()
    
    # Guardar en diferentes formatos
    print("\n💾 Guardando en diferentes formatos...")
    loader.save_to_csv(df_example, 'example_data.csv')
    loader.save_to_json(df_example, 'example_data.json')
    
    # Crear metadatos
    metadata = {
        'description': 'Datos de ejemplo',
        'rows': len(df_example),
        'columns': list(df_example.columns)
    }
    loader.save_metadata('example_data.csv', metadata)
    
    # Listar archivos
    print("\n📁 Archivos en Output:")
    files = loader.list_files()
    for f in files[:5]:  # Mostrar solo primeros 5
        print(f"  - {f.name}")
    
    print("\n" + "="*60)
