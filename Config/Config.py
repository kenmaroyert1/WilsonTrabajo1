"""⚙️ CONFIGURACIÓN CENTRALIZADA DEL PROYECTO

Este módulo es el CEREBRO de configuración del proyecto. Almacena TODAS
las constantes, rutas, parámetros y configuraciones en un solo lugar.

🎯 PROPÓSITO:
   - Evitar "números mágicos" dispersos por el código
   - Facilitar cambios de configuración (un solo lugar para editar)
   - Mantener consistencia en todo el proyecto
   - Documentar qué significa cada parámetro

📋 QUÉ CONTIENE:
   1. Rutas de directorios (datos, salida, figuras)
   2. Parámetros de procesamiento (tamaños de chunk, ventanas)
   3. Definiciones de columnas esperadas
   4. Configuración de visualización (tamaños, colores, DPI)
   5. Funciones de utilidad (crear directorios, mostrar config)

🔧 CÓMO USAR:
   ```python
   from Config.Config import OUTPUT_DIR, CHUNK_SIZE, ensure_directories
   
   ensure_directories()  # Crear directorios si no existen
   print(f"Guardando en: {OUTPUT_DIR}")
   print(f"Procesando con chunks de {CHUNK_SIZE:,} filas")
   ```

💡 CONSEJOS:
   - Importa SOLO lo que necesitas: `from Config.Config import CHUNK_SIZE`
   - NO modifiques constantes en tiempo de ejecución
   - Si algo debe ser configurable, agrégalo aquí
   - Usa MAYÚSCULAS para constantes globales
"""

import os
from pathlib import Path

# ============================================================================
# 📁 RUTAS DEL PROYECTO
# ============================================================================
# Define dónde están ubicados todos los archivos del proyecto

# Ruta raíz del proyecto (directorio donde está este archivo Config.py)
# __file__ es la ruta de este archivo, .parent.parent sube 2 niveles
PROJECT_ROOT = Path(__file__).parent.parent

# Rutas de directorios principales
DATA_DIR = PROJECT_ROOT / "Data"          # Donde están los CSV originales (si existen)
OUTPUT_DIR = PROJECT_ROOT / "Output"      # Donde se guardan TODOS los resultados
FIGURES_DIR = OUTPUT_DIR / "figures"      # Donde se guardan las 11 gráficas PNG

# Archivos específicos (rutas completas)
RAW_DATA_FILE = PROJECT_ROOT / "IntegratedData.csv"              # Dataset original (77MB)
CLEANED_DATA_FILE = OUTPUT_DIR / "IntegratedData_cleaned.csv"    # Dataset después de limpieza

# ============================================================================
# ⚙️ CONFIGURACIÓN DE PROCESAMIENTO
# ============================================================================
# Parámetros que controlan cómo se procesan los datos

# Tamaño de chunk para lectura de archivos grandes
# 100,000 filas = balance perfecto entre memoria y velocidad
# - Más pequeño (50k): Usa menos memoria pero más lento
# - Más grande (200k): Más rápido pero usa más memoria
CHUNK_SIZE = 100_000

# ============================================================================
# 📋 DEFINICIÓN DE COLUMNAS DEL DATASET
# ============================================================================
# Define qué columnas esperamos encontrar y cómo clasificarlas

# Todas las columnas esperadas en el dataset original
EXPECTED_COLUMNS = [
    'date',              # Fecha del registro (YYYY-MM-DD)
    'county',            # Nombre del condado (ej: Los Angeles)
    'state',             # Nombre del estado (ej: California)
    'fips',              # Código FIPS del condado (identificador único)
    'cases',             # Casos acumulados totales
    'deaths',            # Muertes acumuladas totales
    'daily_cases',       # Casos nuevos ese día
    'daily_deaths',      # Muertes nuevas ese día
    'day_of_week',       # Día de la semana (0=Lunes, 6=Domingo)
    'is_weekend',        # 1 si es fin de semana, 0 si no
    'is_holiday',        # 1 si es día feriado, 0 si no
    'retail_recreation', # Cambio % en movilidad a comercios/recreación
    'grocery_pharmacy',  # Cambio % en movilidad a supermercados/farmacias
    'parks',             # Cambio % en movilidad a parques
    'transit',           # Cambio % en uso de transporte público
    'workplaces',        # Cambio % en movilidad a lugares de trabajo
    'residential'        # Cambio % en tiempo en zonas residenciales
]

# Columnas de movilidad (subconjunto de EXPECTED_COLUMNS)
# Estas miden cambios de comportamiento durante la pandemia
MOBILITY_COLUMNS = [
    'retail_recreation',  # Tiendas, restaurantes, cines, museos
    'grocery_pharmacy',   # Supermercados, farmacias (esenciales)
    'parks',              # Parques, playas, espacios públicos
    'transit',            # Estaciones de metro, autobús, tren
    'workplaces',         # Oficinas, fábricas, lugares de trabajo
    'residential'         # Tiempo pasado en casa
]

# Columnas numéricas (para cálculos matemáticos)
# Se excluyen strings como 'county' y 'state'
NUMERIC_COLUMNS = [
    'fips',           # Código numérico
    'cases',          # Acumulados
    'deaths',         # Acumulados
    'daily_cases',    # Diarios
    'daily_deaths',   # Diarios
    'day_of_week',    # 0-6
    'is_weekend',     # 0 o 1 (booleano numérico)
    'is_holiday'      # 0 o 1 (booleano numérico)
] + MOBILITY_COLUMNS  # Agregar también columnas de movilidad (todas son numéricas)

# Columnas de fecha (requieren parsing especial)
DATE_COLUMNS = ['date']

# Columnas categóricas (texto, no numéricas)
CATEGORICAL_COLUMNS = ['county', 'state']

# ============================================================================
# 🧹 CONFIGURACIÓN DE LIMPIEZA
# ============================================================================
# Parámetros para el proceso de limpieza de datos

# Valores que deben considerarse como NaN (vacíos/nulos)
# Incluye variaciones comunes de "vacío" en diferentes sistemas
NULL_VALUES = ['', 'nan', 'NaN', 'NA', 'N/A', 'null', 'NULL', 'None']

# Estrategia de manejo de duplicados
DROP_DUPLICATES = True  # Si True, elimina duplicados; si False, los mantiene
DUPLICATE_SUBSET = ['date', 'county', 'state']  # Columnas para identificar duplicados
# Ejemplo: si hay 2 filas con misma fecha + county + state, se considera duplicado

# ============================================================================
# 📊 CONFIGURACIÓN DE VISUALIZACIÓN
# ============================================================================
# Parámetros que controlan cómo se ven las gráficas

# Configuración general de gráficas
FIGURE_DPI = 100              # Resolución (puntos por pulgada) - Mayor = mejor calidad
FIGURE_FORMAT = 'png'         # Formato de archivo (png, jpg, pdf, svg)
FIGURE_STYLE = 'whitegrid'    # Estilo Seaborn (whitegrid, darkgrid, white, dark, ticks)

# Tamaños de figura por defecto (ancho, alto en pulgadas)
FIGURE_SIZE_DEFAULT = (12, 6)        # Para gráficas estándar
FIGURE_SIZE_LARGE = (14, 7)          # Para gráficas con mucha información
FIGURE_SIZE_HEATMAP = (14, 10)       # Para mapas de calor (más espacio vertical)

# Paleta de colores para diferentes tipos de datos
COLOR_CASES = '#3498db'       # Azul para casos (color frío = dato neutro)
COLOR_DEATHS = '#e74c3c'      # Rojo para muertes (color cálido = gravedad)
COLOR_POSITIVE = '#e67e22'    # Naranja para correlación positiva
COLOR_NEGATIVE = '#27ae60'    # Verde para correlación negativa

# Configuración de mapas de calor (heatmaps)
HEATMAP_CMAP = 'coolwarm'     # Mapa de colores: azul (frío/negativo) a rojo (cálido/positivo)
HEATMAP_CENTER = 0            # Centro de escala de colores (0 = sin correlación)
HEATMAP_VMIN = -1             # Valor mínimo (correlación negativa perfecta)
HEATMAP_VMAX = 1              # Valor máximo (correlación positiva perfecta)

# ============================================================================
# 🔄 CONFIGURACIÓN DE TRANSFORMACIÓN
# ============================================================================
# Parámetros para cálculos de métricas derivadas

# Ventana para promedio móvil (días)
# 7 días = 1 semana completa, elimina ruido de fines de semana
# Cambiar a 14 para suavizado más fuerte, o 3 para más sensibilidad
MOVING_AVERAGE_WINDOW = 7

# Número de top elementos a mostrar en rankings
# Usado en Transform.py para obtener top condados/estados
TOP_N_COUNTIES = 10       # Top 10 condados más afectados
TOP_N_STATES = 10         # Top 10 estados más afectados
TOP_N_MORTALITY = 15      # Top 15 estados con mayor mortalidad

# ============================================================================
# 📋 CONFIGURACIÓN DE LOGGING (para depuración)
# ============================================================================
# Parámetros para registrar eventos del programa

# Nivel de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
# INFO: Mensajes informativos normales (recomendado)
# DEBUG: Mensajes detallados para depuración
LOG_LEVEL = 'INFO'

# Formato de mensajes de log
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# Ejemplo: "2026-02-04 10:30:15 - Config - INFO - Directorios creados"

# Formato de fecha en logs
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

# ============================================================================
# 📝 METADATOS DEL PROYECTO
# ============================================================================
# Información general sobre el proyecto (para documentación y reportes)

PROJECT_NAME = "WilsonTrabajo1"
PROJECT_DESCRIPTION = "Análisis de COVID-19 y Movilidad en EE.UU."
PROJECT_VERSION = "1.0.0"
PROJECT_AUTHOR = "Wilson Team"
PROJECT_YEAR = 2026

# ============================================================================
# 🛠️ FUNCIONES AUXILIARES
# ============================================================================
# Funciones de utilidad que usan las configuraciones anteriores

def ensure_directories():
    """
    🛠️ Crea los directorios necesarios si no existen.
    
    Esta función debe llamarse al inicio de cualquier script que necesite
    guardar archivos. Es seguro llamarla múltiples veces (no da error si
    el directorio ya existe).
    
    Directorios creados:
    - Output/           : Para archivos procesados (CSV, metadatos)
    - Output/figures/   : Para gráficas PNG
    - Data/             : Para datos adicionales (si se necesita)
    
    Ejemplo:
        >>> from Config.Config import ensure_directories
        >>> ensure_directories()
        >>> # Ahora puedes guardar archivos en Output/ y Output/figures/
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)    # Crea Output/ y subdirectorios si no existen
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)   # Crea Output/figures/ si no existe
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)  # Crea Data/ si no existe


def get_config_summary():
    """
    📊 Retorna un resumen legible de la configuración actual.
    
    Útil para:
    - Verificar configuración antes de ejecutar pipeline
    - Guardar metadatos sobre cómo se procesaron los datos
    - Debugging y reportes
    
    Returns:
        dict: Diccionario con configuraciones principales
        
    Ejemplo:
        >>> from Config.Config import get_config_summary
        >>> config = get_config_summary()
        >>> print(f"Procesando: {config['project_name']} v{config['version']}")
        >>> print(f"Chunk size: {config['chunk_size']:,} filas")
    """
    return {
        'project_name': PROJECT_NAME,
        'version': PROJECT_VERSION,
        'raw_data': str(RAW_DATA_FILE),
        'cleaned_data': str(CLEANED_DATA_FILE),
        'chunk_size': CHUNK_SIZE,
        'output_dir': str(OUTPUT_DIR),
        'figures_dir': str(FIGURES_DIR),
        'moving_avg_window': MOVING_AVERAGE_WINDOW,
        'top_n_counties': TOP_N_COUNTIES,
        'top_n_states': TOP_N_STATES,
    }


# ============================================================================
# 🚀 EJECUCIÓN COMO SCRIPT PRINCIPAL
# ============================================================================
# Si ejecutas este archivo directamente (python Config.py), muestra un resumen

if __name__ == "__main__":
    print("="*70)
    print(" ⚙️  CONFIGURACIÓN DEL PROYECTO - WilsonTrabajo1")
    print("="*70)
    
    # Crear directorios necesarios
    print("\n📁 Creando directorios necesarios...")
    ensure_directories()
    print(f"   ✅ {OUTPUT_DIR}")
    print(f"   ✅ {FIGURES_DIR}")
    
    # Mostrar resumen de configuración
    print("\n📊 Resumen de Configuración:")
    print("-"*70)
    config = get_config_summary()
    for key, value in config.items():
        print(f"   {key:20s}: {value}")
    
    print("\n📋 Columnas Esperadas:")
    print(f"   Total: {len(EXPECTED_COLUMNS)} columnas")
    print(f"   - Numéricas: {len(NUMERIC_COLUMNS)}")
    print(f"   - Movilidad: {len(MOBILITY_COLUMNS)}")
    print(f"   - Categóricas: {len(CATEGORICAL_COLUMNS)}")
    print(f"   - Fechas: {len(DATE_COLUMNS)}")
    
    print("\n⚙️  Parámetros de Procesamiento:")
    print(f"   - Chunk size: {CHUNK_SIZE:,} filas")
    print(f"   - Promedio móvil: {MOVING_AVERAGE_WINDOW} días")
    print(f"   - Top condados: {TOP_N_COUNTIES}")
    print(f"   - Top estados: {TOP_N_STATES}")
    
    print("\n📊 Configuración de Visualización:")
    print(f"   - Resolución: {FIGURE_DPI} DPI")
    print(f"   - Formato: {FIGURE_FORMAT}")
    print(f"   - Estilo: {FIGURE_STYLE}")
    
    print("\n" + "="*70)
    print(" ✅ Configuración cargada exitosamente")
    print("="*70)

    
    # Mostrar configuración
    print(f"{'='*60}")
    print(f"Configuración del Proyecto: {PROJECT_NAME}")
    print(f"{'='*60}")
    
    config = get_config_summary()
    for key, value in config.items():
        print(f"{key:20s}: {value}")
    
    print(f"{'='*60}")
