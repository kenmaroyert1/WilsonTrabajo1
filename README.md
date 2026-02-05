# WilsonTrabajo1 - Pipeline ETL para Análisis de COVID-19

## 🚀 Inicio Rápido (Quick Start)

### Requisitos Previos
- Python 3.7 o superior
- Dataset: `IntegratedData.csv` (colocar en la raíz del proyecto)

### Instalación en 3 Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/kenmaroyert1/WilsonTrabajo1.git
cd WilsonTrabajo1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar el pipeline completo
python pipeline.py
```

### ✅ Resultado
Después de ejecutar `pipeline.py`, obtendrás:
- ✔️ Datos limpios: `Output/IntegratedData_cleaned.csv`
- ✔️ Datos transformados: `Output/IntegratedData_transformed.csv`
- ✔️ 11 gráficas profesionales en: `Output/figures/`
- ✔️ Agregaciones: `Output/agregado_nacional.csv`, `top_estados.csv`, `top_condados.csv`

### 📊 Ejecutar Solo Visualizaciones

Si ya tienes los datos procesados:
```python
from Vizualize.plot import *
from Config.Config import OUTPUT_DIR, FIGURES_DIR

# Generar todas las gráficas
crear_serie_temporal_casos(OUTPUT_DIR / "IntegratedData_transformed.csv")
crear_mapa_calor_movilidad(OUTPUT_DIR / "IntegratedData_transformed.csv")
# ... más funciones disponibles
```

---

## 📖 Descripción del Proyecto

Este proyecto implementa un **pipeline ETL completo** para el análisis de datos de COVID-19 en Estados Unidos, combinando información epidemiológica (casos y muertes) con datos de movilidad poblacional.

### 🎯 Objetivo
Procesar, analizar y visualizar grandes volúmenes de datos sobre la pandemia para entender la relación entre los cambios en patrones de movilidad y la propagación del virus.

### 📚 Documentación Adicional
- **[DATASET_INFO.md](DATASET_INFO.md)** - Información detallada sobre el dataset, visualizaciones, casos de uso e interpretación de gráficas

---

## 🔧 Arquitectura del Pipeline ETL

El proyecto sigue una arquitectura modular con 5 etapas principales:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   EXTRACT   │ --> │    CLEAN    │ --> │  TRANSFORM  │ --> │    LOAD     │ --> │  VISUALIZE  │
│   Lectura   │     │  Limpieza   │     │  Análisis   │     │  Guardado   │     │  Gráficas   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### 1. **Extract** - Extracción de Datos
- Lectura eficiente de archivos CSV grandes (77MB+)
- Procesamiento por chunks para optimizar memoria
- Múltiples métodos de extracción (completo, por partes, filtrado)

### 2. **Clean** - Limpieza de Datos
- Normalización de nombres de columnas
- Eliminación de duplicados y valores nulos
- Streaming para archivos grandes (>50MB)

### 3. **Transform** - Transformación y Análisis
- Cálculo de métricas derivadas (tasas, promedios móviles)
- Agregaciones temporales y geográficas
- Detección y manejo de outliers

### 4. **Load** - Persistencia de Datos
- Guardado en múltiples formatos (CSV, Excel, JSON, Parquet)
- Backups automáticos con timestamp
- Gestión de metadatos

### 5. **Visualize** - Generación de Gráficas
- 11 visualizaciones profesionales en español
- Gráficas de alta resolución (300 DPI)
- Interpretaciones detalladas

---

## 📦 Módulos Implementados

### ⚙️ **Config/Config.py** - Configuración Centralizada

**Propósito:** Gestionar toda la configuración del proyecto desde un solo lugar.

**Contiene:**
```python
# Rutas de directorios
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "Data"
OUTPUT_DIR = PROJECT_ROOT / "Output"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Parámetros de procesamiento
CHUNK_SIZE = 100000  # Filas por chunk para archivos grandes
DATE_COLUMN = 'date'
FIGSIZE = (14, 8)
DPI = 300

# Configuración de visualización
COLOR_PALETTE = 'viridis'
STYLE = 'seaborn-v0_8-darkgrid'
```

**Funciones principales:**
- `setup_directories()`: Crea directorios necesarios
- `get_config_summary()`: Muestra resumen de configuración
- `validate_paths()`: Valida existencia de archivos/carpetas

**Cuándo usarlo:**
- Importar constantes en otros módulos
- Cambiar rutas de archivos
- Ajustar parámetros de procesamiento

---

### 📥 **Extract/Extract.py** - Extracción de Datos

**Propósito:** Proporcionar múltiples formas de leer datos del CSV inicial.

**Clase:** `DataExtractor`

**Métodos disponibles:**

1. **`extract_full()`** - Carga completa en memoria
   - Usa cuando: Tienes suficiente RAM (>8GB)
   - Retorna: DataFrame completo

2. **`extract_chunks(chunk_size=100000)`** - Iterador por chunks
   - Usa cuando: Archivo muy grande o poca RAM
   - Retorna: Iterador de DataFrames

3. **`extract_columns(columns)`** - Solo columnas específicas
   - Usa cuando: Solo necesitas algunas columnas
   - Retorna: DataFrame con columnas seleccionadas

4. **`extract_sample(frac=0.1)`** - Muestreo aleatorio
   - Usa cuando: Pruebas rápidas con 10% de datos
   - Retorna: DataFrame con muestra aleatoria

5. **`extract_by_state(states)`** - Filtrar por estados
   - Usa cuando: Solo necesitas datos de ciertos estados
   - Retorna: DataFrame filtrado

6. **`extract_date_range(start, end)`** - Filtrar por fechas
   - Usa cuando: Solo necesitas un período específico
   - Retorna: DataFrame con fechas en el rango

7. **`get_info()`** - Información sin cargar datos
   - Usa cuando: Quieres saber tamaño, columnas sin usar memoria
   - Retorna: Diccionario con metadatos

**Ejemplo de uso:**
```python
from Extract.Extract import DataExtractor

extractor = DataExtractor("IntegratedData.csv")

# Opción 1: Cargar todo
df_completo = extractor.extract_full()

# Opción 2: Procesar por chunks (archivos grandes)
for chunk in extractor.extract_chunks(chunk_size=50000):
    procesar(chunk)

# Opción 3: Solo datos de California
df_california = extractor.extract_by_state(['California'])
```

---

### 🧹 **Extract/Clean/Clean.py** - Limpieza de Datos

**Propósito:** Limpiar y normalizar datos crudos para análisis.

**Qué hace:**

1. **Normalización de columnas:**
   - `Cases` → `cases`
   - `Daily Cases` → `daily_cases`

2. **Limpieza de valores:**
   - Quita espacios en blanco
   - Convierte valores vacíos a NaN
   - Parsea fechas automáticamente

3. **Eliminación de duplicados:**
   - Identifica y elimina filas duplicadas
   - Mantiene primera ocurrencia

4. **Procesamiento por chunks:**
   - Lee en bloques de 100,000 filas
   - Procesa cada bloque independientemente
   - Puede procesar archivos de 10GB+ con 2GB de RAM

**Función principal:**
```python
from Extract.Clean.Clean import clean_csv

clean_csv(
    input_csv="IntegratedData.csv",
    output_csv="Output/IntegratedData_cleaned.csv"
)
```

**Funciones auxiliares:**
- `normalize_column_name(col)`: Normaliza nombre de columna
- `clean_chunk(chunk)`: Limpia un chunk de datos
- `remove_duplicates_chunked()`: Elimina duplicados en streaming

---

### 🔄 **Transform/Transform.py** - Transformación de Datos

**Propósito:** Calcular métricas derivadas y realizar análisis avanzado.

**Clase:** `DataTransformer`

**Transformaciones disponibles:**

1. **Promedios Móviles**
   ```python
   df = transformer.add_moving_average(df, column='daily_cases', window=7)
   # Añade columna: daily_cases_ma7
   ```

2. **Tasas Derivadas**
   ```python
   df = transformer.calculate_mortality_rate(df)
   # Añade: mortality_rate (muertes/casos * 100)
   
   df = transformer.calculate_growth_rate(df, column='cases')
   # Añade: cases_growth_rate
   ```

3. **Agregaciones**
   ```python
   # Agregación por fecha
   df_daily = transformer.aggregate_by_date(df)
   
   # Agregación por estado
   df_state = transformer.aggregate_by_state(df)
   
   # Agregación por condado
   df_county = transformer.aggregate_by_county(df)
   ```

4. **Rankings**
   ```python
   # Top 10 estados con más casos
   top_states = transformer.get_top_states(df, metric='cases', n=10)
   
   # Top 10 condados con más muertes
   top_counties = transformer.get_top_counties(df, metric='deaths', n=10)
   ```

5. **Correlaciones**
   ```python
   # Matriz de correlación
   corr_matrix = transformer.calculate_correlation(df, columns=['cases', 'deaths', 'mobility'])
   ```

6. **Features Temporales**
   ```python
   df = transformer.add_temporal_features(df)
   # Añade: year, month, week, day_of_week, quarter, is_weekend
   ```

7. **Normalización**
   ```python
   # Min-Max (0-1)
   df = transformer.normalize_minmax(df, columns=['cases', 'deaths'])
   
   # Z-score (media=0, std=1)
   df = transformer.normalize_zscore(df, columns=['cases', 'deaths'])
   ```

8. **Detección de Outliers**
   ```python
   # Método IQR (InterQuartile Range)
   df = transformer.remove_outliers_iqr(df, column='cases')
   
   # Método Z-score
   df = transformer.remove_outliers_zscore(df, column='cases', threshold=3)
   ```

**Ejemplo completo:**
```python
from Transform.Transform import DataTransformer
import pandas as pd

transformer = DataTransformer()
df = pd.read_csv("Output/IntegratedData_cleaned.csv")

# Aplicar múltiples transformaciones
df = transformer.add_temporal_features(df)
df = transformer.add_moving_average(df, 'daily_cases', window=7)
df = transformer.calculate_mortality_rate(df)

# Guardar datos transformados
df.to_csv("Output/IntegratedData_transformed.csv", index=False)
```

---

### 💾 **Load/Load.py** - Persistencia de Datos

**Propósito:** Guardar y cargar datos procesados en múltiples formatos.

**Clase:** `DataLoader`

**Formatos soportados:**
- CSV (`.csv`)
- Excel (`.xlsx`)
- JSON (`.json`)
- Parquet (`.parquet`)

**Funciones principales:**

1. **Guardar datos**
   ```python
   from Load.Load import DataLoader
   
   loader = DataLoader(output_dir="Output")
   
   # Guardar en CSV
   loader.save_csv(df, "datos_procesados.csv")
   
   # Guardar en Excel con formato
   loader.save_excel(df, "datos_procesados.xlsx")
   
   # Guardar en JSON
   loader.save_json(df, "datos_procesados.json")
   
   # Guardar en Parquet (más eficiente)
   loader.save_parquet(df, "datos_procesados.parquet")
   ```

2. **Cargar datos**
   ```python
   # Cargar desde CSV
   df = loader.load_csv("datos_procesados.csv")
   
   # Cargar desde Excel
   df = loader.load_excel("datos_procesados.xlsx")
   
   # Cargar desde JSON
   df = loader.load_json("datos_procesados.json")
   
   # Cargar desde Parquet
   df = loader.load_parquet("datos_procesados.parquet")
   ```

3. **Guardado por chunks (archivos grandes)**
   ```python
   loader.save_csv_chunks(df, "datos_grandes.csv", chunk_size=100000)
   ```

4. **Backups automáticos**
   ```python
   loader.save_with_backup(df, "datos_importantes.csv")
   # Crea: datos_importantes_backup_20260205_143022.csv
   ```

5. **Guardar metadatos**
   ```python
   loader.save_metadata(df, "datos_procesados.csv")
   # Crea: datos_procesados_metadata.json con info del dataset
   ```

6. **Gestión de archivos**
   ```python
   # Listar archivos en Output/
   files = loader.list_files()
   
   # Obtener información de un archivo
   info = loader.get_file_info("datos_procesados.csv")
   ```

---

### 📊 **Vizualize/plot.py** - Generación de Visualizaciones

**Propósito:** Generar 11 gráficas profesionales en español para análisis de COVID-19.

**Funciones de visualización:**

1. **`crear_serie_temporal_casos(csv_path)`**
   - Evolución temporal de casos y muertes (eje dual)
   - Archivo: `1_evolucion_casos_muertes.png`

2. **`crear_top_condados(csv_path)`**
   - Top 10 condados con más casos
   - Archivo: `2_top_condados_casos.png`

3. **`crear_scatter_casos_muertes(csv_path)`**
   - Relación casos vs muertes (scatter + tendencia)
   - Archivo: `3_casos_vs_muertes.png`

4. **`crear_correlacion_movilidad(csv_path)`**
   - Correlación movilidad vs casos
   - Archivo: `4_movilidad_correlacion.png`

5. **`crear_comparacion_dias(csv_path)`**
   - Comparación días laborales vs fines de semana
   - Archivo: `5_comparacion_dias.png`

6. **`crear_top_estados(csv_path)`**
   - Top 10 estados más afectados
   - Archivo: `6_top_estados_casos.png`

7. **`crear_tasa_mortalidad_estados(csv_path)`**
   - Tasa de mortalidad por estado (top 15)
   - Archivo: `7_tasa_mortalidad_estados.png`

8. **`crear_evolucion_movilidad(csv_path)`**
   - Evolución temporal de movilidad (todas las categorías)
   - Archivo: `8_evolucion_movilidad.png`

9. **`crear_distribucion_dia_semana(csv_path)`**
   - Distribución de casos y muertes por día de semana
   - Archivo: `9_casos_dia_semana.png`

10. **`crear_promedio_movil(csv_path)`**
    - Promedio móvil de 7 días (casos y muertes)
    - Archivo: `10_promedio_movil.png`

11. **`crear_mapa_calor_correlacion(csv_path)`**
    - Matriz de correlación completa (heatmap)
    - Archivo: `11_mapa_calor_correlacion.png`

**Generar todas las gráficas:**
```python
from Vizualize.plot import generar_todas_las_graficas

generar_todas_las_graficas(
    csv_path="Output/IntegratedData_transformed.csv",
    output_dir="Output/figures"
)
```

**O ejecutar desde línea de comandos:**
```bash
python -m Vizualize.plot --input "Output/IntegratedData_cleaned.csv" --outdir "Output/figures"
```

**Características:**
- Alta resolución (300 DPI)
- Estilo profesional con seaborn
- Todas las etiquetas en español
- Colores optimizados para publicación
- Tamaños de figura configurables

---

### 🚀 **pipeline.py** - Pipeline ETL Completo

**Propósito:** Orquestar todas las etapas del procesamiento en un solo script.

**Qué hace:**
1. ✅ Carga configuración
2. ✅ Extrae datos del CSV original
3. ✅ Limpia datos (chunks)
4. ✅ Aplica transformaciones
5. ✅ Guarda datos procesados
6. ✅ Genera agregaciones
7. ✅ Crea visualizaciones

**Uso básico:**
```bash
# Ejecutar pipeline completo
python pipeline.py

# Ver configuración
python pipeline.py --show-config

# Especificar archivo de entrada
python pipeline.py --input MiArchivo.csv

# Sin archivos intermedios
python pipeline.py --skip-intermediate
```

**Argumentos disponibles:**
- `--input`: Archivo CSV de entrada (default: `IntegratedData.csv`)
- `--output`: Directorio de salida (default: `Output/`)
- `--skip-intermediate`: No guardar archivos intermedios
- `--show-config`: Mostrar configuración y salir
- `--visualize`: Generar solo visualizaciones (sin procesar)

**Flujo del pipeline:**
```python
# 1. Extracción
extractor = DataExtractor(input_file)
df = extractor.extract_full()

# 2. Limpieza
clean_csv(input_file, cleaned_file)
df = pd.read_csv(cleaned_file)

# 3. Transformación
transformer = DataTransformer()
df = transformer.add_temporal_features(df)
df = transformer.add_moving_average(df, 'daily_cases', window=7)
df = transformer.calculate_mortality_rate(df)

# 4. Carga
loader = DataLoader(output_dir)
loader.save_csv(df, "IntegratedData_transformed.csv")

# 5. Agregaciones
nacional = transformer.aggregate_by_date(df)
estados = transformer.get_top_states(df, n=10)
condados = transformer.get_top_counties(df, n=10)

# 6. Visualización
generar_todas_las_graficas(transformed_file, figures_dir)
```

---

## 📁 Estructura del Proyecto

```
WilsonTrabajo1/
├── 📁 Config/                    # ⚙️ Configuración
│   ├── __init__.py
│   └── Config.py                # Constantes y configuración global
│
├── 📁 Extract/                   # 📥 Extracción de datos
│   ├── __init__.py
│   ├── Extract.py               # Clase DataExtractor (7 métodos)
│   └── 📁 Clean/                # 🧹 Limpieza de datos
│       ├── __init__.py
│       └── Clean.py             # Limpieza por chunks
│
├── 📁 Transform/                 # 🔄 Transformación
│   ├── __init__.py
│   └── Transform.py             # Clase DataTransformer (15+ funciones)
│
├── 📁 Load/                      # 💾 Persistencia
│   ├── __init__.py
│   └── Load.py                  # Clase DataLoader (4 formatos)
│
├── 📁 Vizualize/                 # 📊 Visualización
│   ├── __init__.py
│   └── plot.py                  # 11 funciones de gráficas
│
├── 📁 Output/                    # 📂 Archivos de salida
│   ├── __init__.py
│   ├── IntegratedData_cleaned.csv
│   ├── IntegratedData_transformed.csv
│   ├── agregado_nacional.csv
│   ├── top_estados.csv
│   ├── top_condados.csv
│   └── 📁 figures/              # 11 visualizaciones PNG
│       ├── 1_evolucion_casos_muertes.png
│       ├── 2_top_condados_casos.png
│       ├── 3_casos_vs_muertes.png
│       ├── 4_movilidad_correlacion.png
│       ├── 5_comparacion_dias.png
│       ├── 6_top_estados_casos.png
│       ├── 7_tasa_mortalidad_estados.png
│       ├── 8_evolucion_movilidad.png
│       ├── 9_casos_dia_semana.png
│       ├── 10_promedio_movil.png
│       └── 11_mapa_calor_correlacion.png
│
├── pipeline.py                  # 🚀 Pipeline ETL completo
├── IntegratedData.csv           # 📊 Dataset original (77MB)
├── requirements.txt             # 📦 Dependencias Python
├── README.md                    # 📖 Esta documentación (técnica)
└── DATASET_INFO.md              # 📊 Información del dataset (no técnica)
```

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje de programación
- **Pandas** - Manipulación de datos (lectura por chunks, limpieza)
- **NumPy** - Operaciones numéricas
- **Matplotlib** - Visualizaciones base
- **Seaborn** - Gráficas estadísticas avanzadas
- **Git/GitHub** - Control de versiones

---

## 📊 Estado Actual del Proyecto

- ✅ **Configuración:** Módulo completo con todas las constantes
- ✅ **Extracción:** 7 métodos diferentes de lectura
- ✅ **Limpieza:** Procesamiento por chunks implementado
- ✅ **Transformación:** 15+ funciones de análisis
- ✅ **Carga:** Soporte para 4 formatos
- ✅ **Visualización:** 11 gráficas profesionales
- ✅ **Pipeline:** Script integrador funcional
- ✅ **Documentación:** README técnico completo

---

## 🚦 Cómo Empezar a Desarrollar

### 1. Clonar y configurar entorno

```bash
git clone https://github.com/kenmaroyert1/WilsonTrabajo1.git
cd WilsonTrabajo1
pip install -r requirements.txt
```

### 2. Familiarizarse con la configuración

```python
from Config.Config import *

# Ver rutas configuradas
print(f"Root: {PROJECT_ROOT}")
print(f"Data: {DATA_DIR}")
print(f"Output: {OUTPUT_DIR}")

# Ver parámetros
print(f"Chunk size: {CHUNK_SIZE}")
```

### 3. Probar módulos individuales

```python
# Extracción
from Extract.Extract import DataExtractor
extractor = DataExtractor("IntegratedData.csv")
df_sample = extractor.extract_sample(frac=0.01)  # 1% de datos

# Limpieza
from Extract.Clean.Clean import clean_csv
clean_csv("test_input.csv", "test_output.csv")

# Transformación
from Transform.Transform import DataTransformer
transformer = DataTransformer()
df = transformer.add_moving_average(df, 'cases', window=7)

# Visualización
from Vizualize.plot import crear_serie_temporal_casos
crear_serie_temporal_casos("Output/IntegratedData_transformed.csv")
```

### 4. Ejecutar pipeline completo

```bash
python pipeline.py
```

### 5. Verificar resultados

- Revisar `Output/IntegratedData_cleaned.csv`
- Revisar `Output/IntegratedData_transformed.csv`
- Ver gráficas en `Output/figures/`

---

## 🧪 Testing y Debugging

### Probar con datos pequeños

```python
# Usar muestra del 10%
extractor = DataExtractor("IntegratedData.csv")
df_test = extractor.extract_sample(frac=0.1)
df_test.to_csv("test_sample.csv", index=False)

# Ejecutar pipeline con muestra
python pipeline.py --input test_sample.csv
```

### Verificar chunks

```python
from Extract.Extract import DataExtractor

extractor = DataExtractor("IntegratedData.csv")
for i, chunk in enumerate(extractor.extract_chunks(chunk_size=10000)):
    print(f"Chunk {i}: {len(chunk)} filas, {chunk.memory_usage().sum() / 1024**2:.2f} MB")
    if i >= 5:  # Solo primeros 5 chunks
        break
```

### Validar transformaciones

```python
from Transform.Transform import DataTransformer
import pandas as pd

df = pd.read_csv("Output/IntegratedData_cleaned.csv", nrows=1000)
transformer = DataTransformer()

# Antes
print("Antes:", df.columns.tolist())
print("Shape:", df.shape)

# Transformar
df = transformer.add_temporal_features(df)

# Después
print("Después:", df.columns.tolist())
print("Shape:", df.shape)
```

---

## 📖 Documentación Relacionada

- **[DATASET_INFO.md](DATASET_INFO.md)** - Información completa sobre el dataset, visualizaciones, casos de uso e interpretación de gráficas

---

## 👥 Contribuciones

Este es un proyecto académico. Para consultas o sugerencias, contactar al equipo de desarrollo.

---

## 📝 Licencia

Proyecto académico - Universidad

---

## 📞 Contacto

- **Repositorio:** https://github.com/kenmaroyert1/WilsonTrabajo1
- **Autor:** Wilson
- **Curso:** Análisis de Datos / Ciencia de Datos
