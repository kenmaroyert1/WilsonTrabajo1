"""Configuración centralizada del proyecto.

Este módulo contiene todas las configuraciones y constantes utilizadas
en el pipeline de procesamiento de datos COVID-19.
"""

import os
from pathlib import Path

# ============================================================================
# RUTAS DEL PROYECTO
# ============================================================================

# Ruta raíz del proyecto
PROJECT_ROOT = Path(__file__).parent.parent

# Rutas de datos
DATA_DIR = PROJECT_ROOT / "Data"
OUTPUT_DIR = PROJECT_ROOT / "Output"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Archivos de datos
RAW_DATA_FILE = PROJECT_ROOT / "IntegratedData.csv"
CLEANED_DATA_FILE = OUTPUT_DIR / "IntegratedData_cleaned.csv"

# ============================================================================
# CONFIGURACIÓN DE PROCESAMIENTO
# ============================================================================

# Tamaño de chunk para lectura de archivos grandes (número de filas)
CHUNK_SIZE = 100_000

# Columnas esperadas en el dataset
EXPECTED_COLUMNS = [
    'date', 'county', 'state', 'fips', 'cases', 'deaths',
    'daily_cases', 'daily_deaths', 'day_of_week', 'is_weekend', 'is_holiday',
    'retail_recreation', 'grocery_pharmacy', 'parks', 'transit',
    'workplaces', 'residential'
]

# Columnas de movilidad
MOBILITY_COLUMNS = [
    'retail_recreation', 'grocery_pharmacy', 'parks',
    'transit', 'workplaces', 'residential'
]

# Columnas numéricas
NUMERIC_COLUMNS = [
    'fips', 'cases', 'deaths', 'daily_cases', 'daily_deaths',
    'day_of_week', 'is_weekend', 'is_holiday'
] + MOBILITY_COLUMNS

# Columnas de fecha
DATE_COLUMNS = ['date']

# Columnas categóricas
CATEGORICAL_COLUMNS = ['county', 'state']

# ============================================================================
# CONFIGURACIÓN DE LIMPIEZA
# ============================================================================

# Valores a considerar como NaN
NULL_VALUES = ['', 'nan', 'NaN', 'NA', 'N/A', 'null', 'NULL', 'None']

# Estrategia de manejo de duplicados
DROP_DUPLICATES = True
DUPLICATE_SUBSET = ['date', 'county', 'state']  # Columnas para identificar duplicados

# ============================================================================
# CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================

# Configuración de gráficas
FIGURE_DPI = 100
FIGURE_FORMAT = 'png'
FIGURE_STYLE = 'whitegrid'

# Colores para gráficas
COLOR_CASES = '#3498db'      # Azul para casos
COLOR_DEATHS = '#e74c3c'     # Rojo para muertes
COLOR_POSITIVE = '#e67e22'   # Naranja para correlación positiva
COLOR_NEGATIVE = '#27ae60'   # Verde para correlación negativa

# Configuración de mapas de calor
HEATMAP_CMAP = 'coolwarm'
HEATMAP_CENTER = 0
HEATMAP_VMIN = -1
HEATMAP_VMAX = 1

# ============================================================================
# CONFIGURACIÓN DE TRANSFORMACIÓN
# ============================================================================

# Ventana para promedio móvil (días)
MOVING_AVERAGE_WINDOW = 7

# Número de top elementos a mostrar en rankings
TOP_N_COUNTIES = 10
TOP_N_STATES = 10
TOP_N_MORTALITY = 15

# ============================================================================
# CONFIGURACIÓN DE LOGGING
# ============================================================================

# Nivel de logging
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ============================================================================
# METADATOS DEL PROYECTO
# ============================================================================

PROJECT_NAME = "WilsonTrabajo1"
PROJECT_DESCRIPTION = "Análisis de COVID-19 y Movilidad en EE.UU."
PROJECT_VERSION = "1.0.0"
PROJECT_AUTHOR = "Wilson Team"
PROJECT_YEAR = 2026

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def ensure_directories():
    """Crea los directorios necesarios si no existen."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_config_summary():
    """Retorna un resumen de la configuración actual."""
    return {
        'project_name': PROJECT_NAME,
        'version': PROJECT_VERSION,
        'raw_data': str(RAW_DATA_FILE),
        'cleaned_data': str(CLEANED_DATA_FILE),
        'chunk_size': CHUNK_SIZE,
        'output_dir': str(OUTPUT_DIR),
        'figures_dir': str(FIGURES_DIR),
    }


if __name__ == "__main__":
    # Crear directorios necesarios
    ensure_directories()
    
    # Mostrar configuración
    print(f"{'='*60}")
    print(f"Configuración del Proyecto: {PROJECT_NAME}")
    print(f"{'='*60}")
    
    config = get_config_summary()
    for key, value in config.items():
        print(f"{key:20s}: {value}")
    
    print(f"{'='*60}")
