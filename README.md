# WilsonTrabajo1 - Pipeline ETL para Análisis de COVID-19

> 📊 **¿Buscas información sobre el dataset y las visualizaciones?**  
> → Ver **[DATASET_INFO.md](DATASET_INFO.md)** - Información del dataset, 6 casos de uso y 11 visualizaciones explicadas detalladamente

---

## 🚀 Inicio Rápido

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

---

## 📖 Sobre Este Proyecto

Este proyecto implementa un **pipeline ETL completo** para análisis de datos de COVID-19, procesando más de 935,000 registros con información epidemiológica y de movilidad de Estados Unidos.

**Documentación adicional:**
- 📊 **[DATASET_INFO.md](DATASET_INFO.md)** - Para qué sirve el dataset, visualizaciones y casos de uso

---

## 🔧 Arquitectura del Pipeline ETL

El proyecto sigue una arquitectura modular de 5 etapas:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   EXTRACT   │ --> │    CLEAN    │ --> │  TRANSFORM  │ --> │    LOAD     │ --> │  VISUALIZE  │
│   Lectura   │     │  Limpieza   │     │  Análisis   │     │  Guardado   │     │  Gráficas   │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

### Resumen de Etapas

1. **Extract** - Lectura eficiente de CSV (77MB+) con procesamiento por chunks
2. **Clean** - Normalización de columnas, eliminación de duplicados
3. **Transform** - Cálculo de métricas derivadas y agregaciones
4. **Load** - Guardado en múltiples formatos con backups
5. **Visualize** - 11 gráficas profesionales en español (300 DPI)

---

## 📦 Explicación del Código - Módulos

### ⚙️ Config/Config.py - Configuración Centralizada

**¿Qué hace?**
Almacena TODAS las configuraciones del proyecto en un solo lugar.

**Contiene:**
```python
# Rutas de directorios
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "Data"
OUTPUT_DIR = PROJECT_ROOT / "Output"
FIGURES_DIR = OUTPUT_DIR / "figures"

# Parámetros de procesamiento
CHUNK_SIZE = 100000  # Filas por chunk
DATE_COLUMN = 'date'

# Configuración de visualización
FIGSIZE = (14, 8)
DPI = 300
COLOR_PALETTE = 'viridis'
STYLE = 'seaborn-v0_8-darkgrid'
```

**Funciones principales:**
- `setup_directories()` - Crea directorios necesarios
- `get_config_summary()` - Muestra resumen de configuración
- `validate_paths()` - Valida existencia de archivos

**¿Cuándo se usa?**
- Al inicio del pipeline para configurar rutas
- Cuando otros módulos necesitan importar constantes
- Para cambiar parámetros globalmente sin editar múltiples archivos

---

### 📥 Extract/Extract.py - Extracción de Datos

**¿Qué hace?**
Proporciona múltiples formas de leer el archivo CSV de 77MB sin consumir toda la RAM.

**Clase Principal:** `DataExtractor`

**7 Métodos de Extracción:**

1. **`extract_full()`** - Carga completa en memoria
   ```python
   extractor = DataExtractor("IntegratedData.csv")
   df = extractor.extract_full()
   ```

2. **`extract_chunks(chunk_size=100000)`** - Procesar por bloques
   ```python
   for chunk in extractor.extract_chunks(chunk_size=50000):
       procesar(chunk)  # Procesa 50,000 filas a la vez
   ```

3. **`extract_columns(columns)`** - Solo columnas específicas
   ```python
   df = extractor.extract_columns(['date', 'cases', 'deaths'])
   ```

4. **`extract_sample(frac=0.1)`** - Muestreo aleatorio
   ```python
   df_test = extractor.extract_sample(frac=0.1)  # 10% de datos
   ```

5. **`extract_by_state(states)`** - Filtrar por estados
   ```python
   df_ca = extractor.extract_by_state(['California', 'Texas'])
   ```

6. **`extract_date_range(start, end)`** - Rango de fechas
   ```python
   df = extractor.extract_date_range('2021-03-01', '2021-03-31')
   ```

7. **`get_info()`** - Información sin cargar datos
   ```python
   info = extractor.get_info()
   print(f"Tamaño: {info['size_mb']} MB")
   ```

**¿Por qué usar chunks?**
- Archivos grandes no caben en memoria RAM
- Permite procesar datasets de 10GB+ con solo 2GB de RAM
- Más eficiente para operaciones secuenciales

---

### 🧹 Extract/Clean/Clean.py - Limpieza de Datos

**¿Qué hace?**
Limpia y normaliza datos crudos automáticamente usando procesamiento por chunks.

**Función Principal:**
```python
from Extract.Clean.Clean import clean_csv

clean_csv(
    input_csv="IntegratedData.csv",
    output_csv="Output/IntegratedData_cleaned.csv"
)
```

**Proceso de Limpieza:**

1. **Normalización de columnas**
   - `Cases` → `cases` (minúsculas)
   - `Daily Cases` → `daily_cases` (sin espacios)
   - `2021-date` → `date` (sin prefijos)

2. **Limpieza de valores**
   - Elimina espacios: `" Texas "` → `"Texas"`
   - Convierte vacíos a NaN: `""` → `NaN`
   - Parsea fechas: `"2021-01-01"` → `datetime`

3. **Eliminación de duplicados**
   - Detecta filas idénticas
   - Mantiene primera ocurrencia
   - Usa streaming para no cargar todo en memoria

4. **Eliminación de filas vacías**
   - Detecta filas donde TODAS las columnas son NaN
   - Las elimina para reducir tamaño del archivo

**¿Cómo funciona el procesamiento por chunks?**
```python
# Lee 100,000 filas a la vez
for chunk in pd.read_csv(input_csv, chunksize=100000):
    chunk_limpio = clean_chunk(chunk)
    chunk_limpio.to_csv(output_csv, mode='append')
```

**Ventajas:**
- Procesa archivos de cualquier tamaño
- Memoria constante (no crece con el archivo)
- Más rápido que cargar todo en memoria

---

### 🔄 Transform/Transform.py - Transformación de Datos

**¿Qué hace?**
Calcula métricas derivadas, agrega datos y realiza análisis estadístico.

**Clase Principal:** `DataTransformer`

**Funciones de Transformación:**

#### 1. Promedios Móviles
```python
transformer = DataTransformer()
df = transformer.add_moving_average(df, column='daily_cases', window=7)
# Añade columna: daily_cases_ma7 (promedio de 7 días)
```

**¿Para qué?** Suavizar fluctuaciones diarias y ver tendencias reales.

#### 2. Tasas Derivadas
```python
# Tasa de mortalidad
df = transformer.calculate_mortality_rate(df)
# Añade: mortality_rate = (muertes / casos) * 100

# Tasa de crecimiento
df = transformer.calculate_growth_rate(df, column='cases')
# Añade: cases_growth_rate = cambio porcentual diario
```

**¿Para qué?** Comparar severidad entre regiones sin depender del tamaño poblacional.

#### 3. Agregaciones
```python
# Agregación por fecha (suma nacional diaria)
df_nacional = transformer.aggregate_by_date(df)

# Agregación por estado
df_estados = transformer.aggregate_by_state(df)

# Agregación por condado
df_condados = transformer.aggregate_by_county(df)
```

**¿Para qué?** Análisis a diferentes niveles geográficos.

#### 4. Rankings
```python
# Top 10 estados con más casos
top_10 = transformer.get_top_states(df, metric='cases', n=10)

# Top 10 condados con más muertes
top_10_condados = transformer.get_top_counties(df, metric='deaths', n=10)
```

**¿Para qué?** Identificar zonas más afectadas.

#### 5. Correlaciones
```python
# Matriz de correlación
corr = transformer.calculate_correlation(
    df, 
    columns=['cases', 'deaths', 'mobility_retail', 'mobility_transit']
)
```

**¿Para qué?** Entender relaciones entre variables (movilidad → casos).

#### 6. Features Temporales
```python
df = transformer.add_temporal_features(df)
# Añade: year, month, week, day_of_week, quarter, is_weekend
```

**¿Para qué?** Detectar patrones estacionales y sesgos de reporte.

#### 7. Normalización
```python
# Min-Max (escala 0-1)
df = transformer.normalize_minmax(df, columns=['cases'])

# Z-score (media=0, desv=1)
df = transformer.normalize_zscore(df, columns=['cases'])
```

**¿Para qué?** Machine learning y comparación entre variables con diferentes escalas.

#### 8. Detección de Outliers
```python
# Método IQR (rango intercuartil)
df = transformer.remove_outliers_iqr(df, column='cases')

# Método Z-score (desviaciones estándar)
df = transformer.remove_outliers_zscore(df, column='cases', threshold=3)
```

**¿Para qué?** Eliminar datos anómalos que distorsionan análisis.

---

### 💾 Load/Load.py - Persistencia de Datos

**¿Qué hace?**
Guarda y carga datos procesados en múltiples formatos con backups automáticos.

**Clase Principal:** `DataLoader`

**Formatos Soportados:**
- CSV (`.csv`) - Compatible, liviano
- Excel (`.xlsx`) - Para usuarios no técnicos
- JSON (`.json`) - APIs y web
- Parquet (`.parquet`) - Más eficiente (compresión y velocidad)

**Guardar Datos:**
```python
loader = DataLoader(output_dir="Output")

# CSV
loader.save_csv(df, "datos_procesados.csv")

# Excel con formato
loader.save_excel(df, "reporte.xlsx")

# JSON
loader.save_json(df, "api_data.json")

# Parquet (más rápido, menor tamaño)
loader.save_parquet(df, "datos.parquet")
```

**Cargar Datos:**
```python
df = loader.load_csv("datos_procesados.csv")
df = loader.load_excel("reporte.xlsx")
df = loader.load_json("api_data.json")
df = loader.load_parquet("datos.parquet")
```

**Funciones Avanzadas:**

1. **Guardado por chunks (archivos grandes)**
   ```python
   loader.save_csv_chunks(df, "datos_grandes.csv", chunk_size=100000)
   ```

2. **Backups automáticos**
   ```python
   loader.save_with_backup(df, "datos_importantes.csv")
   # Crea: datos_importantes_backup_20260205_143022.csv
   ```

3. **Guardar metadatos**
   ```python
   loader.save_metadata(df, "datos.csv")
   # Crea: datos_metadata.json con info del dataset
   ```

4. **Listar archivos**
   ```python
   files = loader.list_files()  # Lista todos los archivos en Output/
   info = loader.get_file_info("datos.csv")  # Info de un archivo
   ```

---

### 📊 Vizualize/plot.py - Generación de Visualizaciones

**¿Qué hace?**
Genera automáticamente 11 gráficas profesionales en español de alta resolución.

**Generar Todas las Gráficas:**
```python
from Vizualize.plot import generar_todas_las_graficas

generar_todas_las_graficas(
    csv_path="Output/IntegratedData_transformed.csv",
    output_dir="Output/figures"
)
```

**O desde línea de comandos:**
```bash
python -m Vizualize.plot --input "Output/IntegratedData_cleaned.csv" --outdir "Output/figures"
```

**11 Funciones de Visualización:**

1. `crear_serie_temporal_casos()` - Evolución temporal nacional
2. `crear_top_condados()` - Top 10 condados
3. `crear_scatter_casos_muertes()` - Relación casos vs muertes
4. `crear_correlacion_movilidad()` - Correlación movilidad-casos
5. `crear_comparacion_dias()` - Días laborales vs fines de semana
6. `crear_top_estados()` - Top 10 estados
7. `crear_tasa_mortalidad_estados()` - Tasa de mortalidad por estado
8. `crear_evolucion_movilidad()` - Series temporales de movilidad
9. `crear_distribucion_dia_semana()` - Distribución por día
10. `crear_promedio_movil()` - Promedio móvil de 7 días
11. `crear_mapa_calor_correlacion()` - Matriz de correlación

**Características de las gráficas:**
- Alta resolución (300 DPI) - Listas para publicación
- Estilo profesional con seaborn
- Todas las etiquetas en español
- Colores optimizados y accesibles
- Guardado automático en PNG

**Ejemplo de uso individual:**
```python
from Vizualize.plot import crear_serie_temporal_casos

crear_serie_temporal_casos(
    csv_path="Output/IntegratedData_transformed.csv",
    output_path="Output/figures/1_evolucion_casos_muertes.png"
)
```

---

### 🚀 pipeline.py - Orquestador del Pipeline ETL

**¿Qué hace?**
Ejecuta todas las etapas del pipeline en el orden correcto automáticamente.

**Ejecución:**
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

**Flujo Completo:**
```python
# 1. Configuración
from Config.Config import *
setup_directories()

# 2. Extracción
from Extract.Extract import DataExtractor
extractor = DataExtractor("IntegratedData.csv")
df = extractor.extract_full()

# 3. Limpieza
from Extract.Clean.Clean import clean_csv
clean_csv("IntegratedData.csv", "Output/IntegratedData_cleaned.csv")

# 4. Transformación
from Transform.Transform import DataTransformer
transformer = DataTransformer()
df = pd.read_csv("Output/IntegratedData_cleaned.csv")
df = transformer.add_temporal_features(df)
df = transformer.add_moving_average(df, 'daily_cases', window=7)
df = transformer.calculate_mortality_rate(df)

# 5. Carga
from Load.Load import DataLoader
loader = DataLoader("Output")
loader.save_csv(df, "IntegratedData_transformed.csv")

# 6. Agregaciones
nacional = transformer.aggregate_by_date(df)
estados = transformer.get_top_states(df, n=10)
condados = transformer.get_top_counties(df, n=10)
loader.save_csv(nacional, "agregado_nacional.csv")
loader.save_csv(estados, "top_estados.csv")
loader.save_csv(condados, "top_condados.csv")

# 7. Visualización
from Vizualize.plot import generar_todas_las_graficas
generar_todas_las_graficas(
    "Output/IntegratedData_transformed.csv",
    "Output/figures"
)
```

**Argumentos de línea de comandos:**
- `--input`: Archivo CSV de entrada (default: `IntegratedData.csv`)
- `--output`: Directorio de salida (default: `Output/`)
- `--skip-intermediate`: No guardar archivos intermedios
- `--show-config`: Mostrar configuración y salir
- `--visualize`: Generar solo visualizaciones

---

## 📁 Estructura del Proyecto

```
WilsonTrabajo1/
├── Config/
│   ├── __init__.py
│   └── Config.py              # ⚙️ Configuración centralizada
│
├── Extract/
│   ├── __init__.py
│   ├── Extract.py            # 📥 7 métodos de extracción
│   └── Clean/
│       ├── __init__.py
│       └── Clean.py          # 🧹 Limpieza por chunks
│
├── Transform/
│   ├── __init__.py
│   └── Transform.py          # 🔄 15+ transformaciones
│
├── Load/
│   ├── __init__.py
│   └── Load.py               # 💾 4 formatos + backups
│
├── Vizualize/
│   ├── __init__.py
│   └── plot.py               # 📊 11 gráficas profesionales
│
├── Output/
│   ├── IntegratedData_cleaned.csv
│   ├── IntegratedData_transformed.csv
│   ├── agregado_nacional.csv
│   ├── top_estados.csv
│   ├── top_condados.csv
│   └── figures/              # 11 visualizaciones PNG
│
├── pipeline.py               # 🚀 Orquestador principal
├── IntegratedData.csv        # 📊 Dataset original (77MB)
├── requirements.txt          # 📦 Dependencias
├── README.md                 # 📖 Esta documentación (código)
└── DATASET_INFO.md           # 📊 Info del dataset + gráficas
```

---

## 🛠️ Tecnologías Utilizadas

- **Python 3.x** - Lenguaje de programación
- **Pandas** - Manipulación de datos y procesamiento por chunks
- **NumPy** - Operaciones numéricas y álgebra lineal
- **Matplotlib** - Visualizaciones base
- **Seaborn** - Gráficas estadísticas avanzadas

---

## 🚦 Guía para Desarrolladores

### 1. Clonar y configurar

```bash
git clone https://github.com/kenmaroyert1/WilsonTrabajo1.git
cd WilsonTrabajo1
pip install -r requirements.txt
```

### 2. Familiarizarse con la configuración

```python
from Config.Config import *

print(f"Root: {PROJECT_ROOT}")
print(f"Chunk size: {CHUNK_SIZE}")
```

### 3. Probar módulos individuales

```python
# Extracción
from Extract.Extract import DataExtractor
extractor = DataExtractor("IntegratedData.csv")
df_sample = extractor.extract_sample(frac=0.01)

# Transformación
from Transform.Transform import DataTransformer
transformer = DataTransformer()
df = transformer.add_moving_average(df, 'cases', window=7)
```

### 4. Ejecutar pipeline

```bash
python pipeline.py
```

### 5. Verificar resultados

- `Output/IntegratedData_cleaned.csv` - Datos limpios
- `Output/IntegratedData_transformed.csv` - Datos transformados
- `Output/figures/` - 11 gráficas PNG

---

## 🧪 Testing y Debugging

### Probar con muestra pequeña

```python
# Usar solo 1% de datos
extractor = DataExtractor("IntegratedData.csv")
df_test = extractor.extract_sample(frac=0.01)
df_test.to_csv("test_sample.csv", index=False)

# Ejecutar pipeline con muestra
python pipeline.py --input test_sample.csv
```

### Verificar procesamiento por chunks

```python
extractor = DataExtractor("IntegratedData.csv")
for i, chunk in enumerate(extractor.extract_chunks(chunk_size=10000)):
    print(f"Chunk {i}: {len(chunk)} filas")
    if i >= 5:
        break
```

### Validar transformaciones

```python
transformer = DataTransformer()
df = pd.read_csv("Output/IntegratedData_cleaned.csv", nrows=1000)

print("Antes:", df.shape)
df = transformer.add_temporal_features(df)
print("Después:", df.shape)
print("Nuevas columnas:", df.columns.tolist())
```

---

## 📖 Documentación Relacionada

- 📊 **[DATASET_INFO.md](DATASET_INFO.md)** - Para qué sirve el dataset, visualizaciones con explicaciones, casos de uso reales

---

## 📞 Contacto

- **Repositorio:** https://github.com/kenmaroyert1/WilsonTrabajo1
- **Proyecto académico** - Universidad
