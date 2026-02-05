# WilsonTrabajo1 - Análisis de COVID-19 y Movilidad en EE.UU.

## 📊 Descripción del Proyecto

Este proyecto realiza un análisis exhaustivo de datos de COVID-19 en Estados Unidos, combinando información epidemiológica (casos y muertes) con datos de movilidad poblacional. El objetivo es entender cómo los cambios en los patrones de movilidad afectaron la propagación del virus durante la pandemia.

### 🗂️ Sobre el Dataset

**Fuente de Datos:** Dataset integrado que combina múltiples fuentes de información pública sobre COVID-19.

**Contenido del Dataset (`IntegratedData.csv`):**
- **Datos Epidemiológicos:** Casos confirmados, muertes, casos diarios y muertes diarias por condado y estado
- **Datos Geográficos:** Códigos FIPS, nombres de condados y estados
- **Datos Temporales:** Fechas, día de la semana, fines de semana, días feriados
- **Datos de Movilidad:** Cambios porcentuales en visitas a:
  - Comercios y lugares de recreación
  - Supermercados y farmacias
  - Parques
  - Estaciones de transporte público
  - Lugares de trabajo
  - Zonas residenciales

**Período de Datos:** 2021 (inicio de la pandemia)

**Alcance Geográfico:** Todos los condados de Estados Unidos (~3,100 condados)

**Tamaño:** ~77 MB con más de 935,000 registros

### 🎯 ¿Para Qué Sirve Este Dataset?

Este dataset y sus visualizaciones son útiles para:

1. **Análisis Epidemiológico:**
   - Identificar patrones temporales de la pandemia (olas, picos)
   - Comparar severidad entre regiones
   - Analizar tasas de mortalidad por área geográfica

2. **Políticas de Salud Pública:**
   - Evaluar efectividad de medidas de confinamiento
   - Identificar áreas que requieren más recursos sanitarios
   - Planificar estrategias de respuesta a futuras pandemias

3. **Estudios de Comportamiento Social:**
   - Entender cómo cambiaron los patrones de movilidad
   - Analizar correlación entre movilidad y contagios
   - Estudiar diferencias entre días laborales y fines de semana

4. **Investigación Académica:**
   - Modelos predictivos de propagación viral
   - Estudios de correlación entre variables socioeconómicas
   - Análisis de series temporales

5. **Toma de Decisiones:**
   - Empresas: planificación de operaciones durante crisis sanitarias
   - Gobiernos: asignación de recursos y comunicación pública
   - Instituciones educativas: políticas de apertura/cierre

## 🔧 Procesamiento de Datos

Este repositorio implementa un **pipeline ETL completo** de procesamiento:

1. **Extracción (Extract):** Lectura y extracción de datos desde archivos CSV grandes
2. **Limpieza (Clean):** Normalización de columnas, eliminación de duplicados, manejo de valores nulos
3. **Transformación (Transform):** Cálculo de métricas derivadas, agregaciones y análisis
4. **Carga (Load):** Guardado de datos procesados en múltiples formatos
5. **Visualización (Visualize):** Generación de 11 gráficas profesionales en español

### 📦 Módulos Implementados

#### **Config.py** - Configuración Centralizada
Gestiona toda la configuración del proyecto:
- 📁 Rutas de directorios (datos, salida, figuras)
- ⚙️ Parámetros de procesamiento (tamaño de chunks: 100,000 filas)
- 📊 Configuración de visualización (tamaños de figura, DPI, paletas de colores)
- 📝 Definición de columnas esperadas y tipos de datos
- 🛠️ Funciones de utilidad (creación de directorios, resumen de configuración)

#### **Extract.py** - Extracción de Datos
Clase `DataExtractor` con múltiples métodos de extracción:
- `extract_full()`: Carga completa de datos en memoria
- `extract_chunks()`: Iterador para procesamiento por chunks
- `extract_columns()`: Extracción de columnas específicas
- `extract_sample()`: Muestreo aleatorio del dataset
- `extract_by_state()`: Filtrado por estado(s)
- `extract_date_range()`: Filtrado por rango de fechas
- `get_info()`: Información del archivo sin cargar datos

#### **Clean.py** - Limpieza de Datos
Procesamiento robusto para archivos grandes:
- ✅ Procesamiento por chunks (para archivos >50MB)
- ✅ Normalización de nombres de columnas (minúsculas, sin espacios)
- ✅ Eliminación de espacios en blanco en strings
- ✅ Conversión de valores vacíos a NaN
- ✅ Parsing de fechas automático
- ✅ Eliminación de filas duplicadas
- ✅ Eliminación de filas completamente vacías
- ✅ Memoria eficiente con streaming

**Resultado:** Dataset limpio guardado en `Output/IntegratedData_cleaned.csv`

#### **Transform.py** - Transformación de Datos
Clase `DataTransformer` con análisis avanzado:
- 📈 **Promedios Móviles:** Suavizado de series temporales (ventanas configurables)
- 📊 **Tasas Derivadas:** Mortalidad, crecimiento, cambios porcentuales
- 🔢 **Agregaciones:** Por fecha, estado, condado
- 🏆 **Rankings:** Top N estados/condados por cualquier métrica
- 🔗 **Correlaciones:** Matrices de correlación entre variables
- 📅 **Features Temporales:** Año, mes, semana, día, trimestre
- 🔧 **Normalización:** MinMax y Z-score
- 🚫 **Outliers:** Detección y remoción (IQR y Z-score)

#### **Load.py** - Carga y Persistencia
Clase `DataLoader` para guardar/cargar datos:
- 💾 **Formatos Múltiples:** CSV, Excel, JSON, Parquet
- 📦 **Procesamiento Chunked:** Guardado por chunks para archivos grandes
- 🔄 **Backups Automáticos:** Creación de copias de seguridad con timestamp
- 📋 **Metadatos:** Guardado de información sobre los datasets
- 📁 **Gestión de Archivos:** Listado, información, organización

#### **pipeline.py** - Pipeline ETL Completo
Script integrador que ejecuta todo el flujo:
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

**El pipeline ejecuta:**
1. ✅ Extracción y limpieza de datos (chunks)
2. ✅ Transformaciones (promedios móviles, tasas, features)
3. ✅ Carga de datos transformados (CSV + metadatos + backup)
4. ✅ Análisis y agregaciones (nacional, estados, condados)
5. ✅ Generación de archivos intermedios útiles

## 📊 Estado Actual del Proyecto

- ✅ **Configuración:** Módulo completo con todas las constantes
- ✅ **Extracción:** 7 métodos diferentes de lectura de datos
- ✅ **Limpieza:** Procesamiento por chunks implementado
- ✅ **Transformación:** 15+ funciones de análisis y transformación
- ✅ **Carga:** Soporte para 4 formatos de archivo
- ✅ **Visualización:** 11 gráficas profesionales en español
- ✅ **Pipeline:** Script integrador completo funcional
- ✅ **Documentación:** README exhaustivo con ejemplos

## Visualizaciones Generadas (11 gráficas en español)

### 1️⃣ Evolución Temporal de Casos y Muertes (Nacional)
**Archivo:** `1_evolucion_casos_muertes.png`

**Qué muestra:** Gráfica de líneas doble (eje Y dual) que muestra la suma nacional diaria de casos y muertes a lo largo del tiempo.

**Interpretación:** 
- Permite identificar olas/picos de la pandemia
- Observar la relación temporal entre casos y muertes
- Las muertes suelen seguir a los casos con un retraso de ~2-3 semanas

**¿Qué nos dice esta gráfica?**
Esta visualización es fundamental para entender la cronología de la pandemia. Los picos azules (casos) anticipan picos rojos (muertes), lo que ayuda a:
- Predecir carga hospitalaria futura
- Evaluar si las medidas de salud pública están funcionando
- Identificar cuándo comienza y termina cada ola de contagios

**Utilidad práctica:** Hospitales pueden prepararse para picos de muertes 2-3 semanas después de picos de casos.

### 2️⃣ Top 10 Condados con Más Casos Acumulados
**Archivo:** `2_top_condados_casos.png`

**Qué muestra:** Gráfica de barras horizontales mostrando los 10 condados con mayor número de casos totales, incluyendo nombre del estado.

**Interpretación:**
- Identifica las áreas más afectadas por la pandemia
- Condados urbanos grandes típicamente tienen más casos debido a mayor densidad poblacional
- Útil para priorizar recursos de salud pública

**¿Qué nos dice esta gráfica?**
Muestra las "zonas calientes" de la pandemia. Los condados con más casos suelen ser:
- Áreas metropolitanas grandes (Los Angeles, Nueva York, Chicago)
- Centros de transporte y comercio
- Zonas con mayor densidad poblacional

**Utilidad práctica:** 
- Gobiernos pueden dirigir vacunas y recursos médicos a estas áreas prioritarias
- Empresas pueden ajustar operaciones según riesgo por zona
- Investigadores pueden estudiar factores comunes en áreas más afectadas

### 3️⃣ Relación entre Casos Diarios y Muertes Diarias
**Archivo:** `3_casos_vs_muertes.png`

**Qué muestra:** Diagrama de dispersión con línea de tendencia mostrando la correlación entre casos diarios y muertes diarias.

**Interpretación:**
- Muestra la tasa de letalidad implícita (pendiente de la línea)
- Puntos dispersos indican variabilidad por factores como edad, acceso a salud, etc.
- Tendencia positiva esperada: más casos → más muertes

**¿Qué nos dice esta gráfica?**
La pendiente de la línea roja muestra la "letalidad promedio" del virus. Si la línea es muy empinada, significa alta mortalidad relativa. La dispersión de puntos indica que hay muchos factores adicionales:
- Calidad del sistema de salud local
- Demografía (áreas con población mayor tienen más muertes)
- Acceso a tratamientos y vacunas
- Variantes del virus circulantes

**Utilidad práctica:**
- Comparar letalidad entre diferentes períodos
- Evaluar efectividad de tratamientos (si la pendiente disminuye con el tiempo)
- Identificar outliers que requieren investigación especial

### 4️⃣ Impacto de Cambios en Movilidad sobre Casos Nuevos
**Archivo:** `4_movilidad_correlacion.png`

**Qué muestra:** Gráfica de barras mostrando correlaciones entre diferentes tipos de movilidad (comercios, supermercados, parques, transporte, trabajo, residencial) y casos diarios.

**Interpretación:**
- **Barras verdes (negativas):** Menos actividad = menos casos (ej: más tiempo en casa)
- **Barras naranjas (positivas):** Más actividad = más casos (ej: más visitas a tiendas)
- Ayuda a entender qué comportamientos reducen/aumentan contagios

**¿Qué nos dice esta gráfica?**
Esta es una de las gráficas más importantes para políticas públicas. Muestra qué cambios en comportamiento están correlacionados con casos:

- **Correlación negativa (buena):** Aumento en tiempo residencial (quedarse en casa) reduce casos
- **Correlación positiva (esperada):** Más visitas a comercios y lugares públicos aumentan casos
- **Transporte público:** Alta correlación positiva porque implica cercanía física prolongada

**Utilidad práctica:**
- Diseñar medidas de confinamiento efectivas (enfocarse en reducir actividades con mayor correlación)
- Evaluar impacto de políticas (¿funcionó el cierre de comercios?)
- Educación pública: comunicar qué actividades son más riesgosas
- Empresas: decidir políticas de trabajo remoto basadas en datos

### 5️⃣ Comparación: Días Laborales vs Fines de Semana
**Archivo:** `5_comparacion_dias.png`

**Qué muestra:** Dos gráficas de barras comparando promedios de casos y muertes en días laborales versus fines de semana.

**Interpretación:**
- Identifica patrones de reporte (algunos lugares reportan menos en fines de semana)
- Puede reflejar diferencias reales en comportamiento social
- Útil para ajustar modelos predictivos

**¿Qué nos dice esta gráfica?**
Muestra un sesgo importante en los datos: los fines de semana típicamente tienen menos casos reportados, pero NO necesariamente menos contagios reales. Esto se debe a:

- **Efecto administrativo:** Menos personal trabajando en laboratorios y oficinas de salud
- **Retraso en reportes:** Los casos del fin de semana se reportan el lunes/martes
- **Comportamiento real:** Menos gente va al médico en fin de semana

**Utilidad práctica:**
- Modelos predictivos deben ajustar por día de la semana
- No entrar en pánico por "bajadas" artificiales los domingos
- Usar promedios de 7 días en lugar de datos diarios crudos
- Periodistas y comunicadores deben reportar tendencias, no fluctuaciones diarias

### 6️⃣ Top 10 Estados Más Afectados
**Archivo:** `6_top_estados_casos.png`

**Qué muestra:** Gráfica de barras horizontales mostrando los 10 estados con mayor número de casos totales acumulados.

**Interpretación:**
- Compara el impacto de la pandemia a nivel estatal
- Estados más poblados y urbanos típicamente tienen más casos
- Útil para análisis de políticas públicas estatales

**¿Qué nos dice esta gráfica?**
Escalada a nivel estatal, muestra qué estados fueron más golpeados por la pandemia. Factores que explican diferencias:

- **Población:** Estados como California, Texas, Florida tienen más casos por ser más poblados
- **Densidad urbana:** Estados con grandes metrópolis tienen más transmisión
- **Conectividad:** Estados con aeropuertos principales recibieron casos más temprano
- **Políticas locales:** Estados con restricciones más estrictas pueden tener menos casos

**Utilidad práctica:**
- Comparar efectividad de políticas estatales diferentes
- Asignar recursos federales proporcionalmente
- Estudios de caso: ¿por qué algunos estados lo hicieron mejor que otros?
- Planificación para futuras pandemias a nivel estatal

### 7️⃣ Tasa de Mortalidad por Estado
**Archivo:** `7_tasa_mortalidad_estados.png`

**Qué muestra:** Top 15 estados con mayor porcentaje de muertes respecto a casos (tasa de letalidad).

**Interpretación:**
- Identifica estados con mayor severidad relativa
- Puede indicar diferencias en acceso a salud, demografía, o calidad de atención
- Rojo más intenso = mayor tasa de mortalidad

**¿Qué nos dice esta gráfica?**
Esta gráfica es MÁS importante que el número absoluto de casos, porque muestra la **severidad relativa** de la pandemia. Un estado puede tener pocos casos pero alta mortalidad, indicando:

- **Sistema de salud saturado:** Hospitales sin capacidad
- **Población vulnerable:** Mayor proporción de personas mayores o con comorbilidades
- **Acceso limitado a tratamientos:** Menos acceso a antivirales, oxígeno, UCI
- **Variantes más letales:** Algunas variantes del virus son más mortales
- **Retraso en diagnóstico:** Casos detectados cuando ya están graves

**Utilidad práctica:**
- Priorizar mejoras en infraestructura de salud en estados con alta letalidad
- Investigar qué están haciendo bien los estados con baja letalidad
- Dirigir vacunas y tratamientos a poblaciones vulnerables en estados críticos
- Análisis económico: impacto en productividad y costos sanitarios

### 8️⃣ Evolución de Movilidad en el Tiempo
**Archivo:** `8_evolucion_movilidad.png`

**Qué muestra:** Series temporales de cambios en movilidad para diferentes categorías (suavizado con promedio de 7 días).

**Interpretación:**
- Muestra cómo cambió el comportamiento durante la pandemia
- Caídas pronunciadas = confinamientos/restricciones
- Recuperación gradual = normalización de actividades
- La línea residencial aumenta cuando otras disminuyen

**¿Qué nos dice esta gráfica?**
Esta es una "radiografía del comportamiento social" durante la pandemia. Cuenta la historia de cómo la gente cambió sus hábitos:

**Fase 1 - Confinamiento:** Todas las líneas caen excepto residencial (la gente se queda en casa)
**Fase 2 - Reapertura gradual:** Las líneas empiezan a subir, especialmente supermercados (esenciales)
**Fase 3 - Nueva normalidad:** Patrones se estabilizan pero no vuelven al 100% pre-pandemia

**Detalles importantes:**
- **Parques:** Muy variable (depende del clima y restricciones locales)
- **Transporte público:** Recuperación lenta (la gente prefiere auto por miedo al contagio)
- **Trabajo:** Muchas empresas adoptaron trabajo remoto permanente

**Utilidad práctica:**
- Empresas de transporte pueden planificar servicios según demanda real
- Comercios pueden ajustar horarios y personal
- Gobiernos locales pueden evaluar cumplimiento de restricciones
- Economistas pueden medir impacto en sectores específicos (turismo, retail, etc.)

### 9️⃣ Distribución por Día de la Semana
**Archivo:** `9_casos_dia_semana.png`

**Qué muestra:** Dos gráficas mostrando promedio de casos y muertes para cada día de la semana (Lunes a Domingo).

**Interpretación:**
- Identifica sesgos en reportes (ej: menos reportes los fines de semana)
- Azul/Morado = días laborales, Rojo/Naranja = fines de semana
- Útil para corregir modelos por efectos de calendario

**¿Qué nos dice esta gráfica?**
Detalla día por día el patrón semanal de reportes y casos reales. Observaciones típicas:

**Lunes/Martes:** Picos artificiales porque se reportan casos acumulados del fin de semana
**Miércoles-Viernes:** Datos más estables y confiables
**Sábado/Domingo:** Caída en reportes (menos personal administrativo trabajando)

**Diferencia entre casos y muertes:**
- Casos: Mayor variabilidad semanal (más dependiente de reportes administrativos)
- Muertes: Menos variabilidad (eventos más críticos se reportan más consistentemente)

**Utilidad práctica:**
- **Para analistas:** No comparar lunes con domingo, usar semanas completas
- **Para modelos predictivos:** Incluir variables dummy de día de la semana
- **Para comunicación pública:** Reportar promedios de 7 días, no picos/valles diarios
- **Para planificación hospitalaria:** Anticipar que los lunes tendrán más diagnósticos acumulados

### 🔟 Promedio Móvil de Casos (7 días)
**Archivo:** `10_promedio_movil.png`

**Qué muestra:** Dos gráficas con datos diarios (línea tenue) y promedio móvil de 7 días (línea gruesa) para casos y muertes.

**Interpretación:**
- Suaviza fluctuaciones diarias y resalta tendencias reales
- Facilita identificar inicio/fin de olas
- El promedio móvil es más confiable para análisis de tendencias

**¿Qué nos dice esta gráfica?**
Esta es la versión "limpia" de los datos diarios. El promedio móvil de 7 días elimina:

- **Ruido del fin de semana:** Ya no vemos bajadas artificiales los domingos
- **Picos administrativos:** Los lunes ya no se ven inflados artificialmente
- **Fluctuaciones aleatorias:** Eventos únicos (ej: un brote en una prisión) no distorsionan la tendencia

**¿Por qué 7 días?**
- Captura un ciclo semanal completo
- Es el estándar usado por CDC, OMS y medios de comunicación
- Permite comparaciones internacionales

**Cómo leerla:**
- **Línea sube:** La pandemia está empeorando (ola creciente)
- **Línea baja:** La pandemia está mejorando (ola en descenso)
- **Línea plana:** Situación estable (meseta)
- **Cambio de pendiente:** Momento crucial para decisiones de política pública

**Utilidad práctica:**
- **Gobiernos:** Decidir cuándo implementar o levantar restricciones
- **Hospitales:** Planificar capacidad con 1-2 semanas de anticipación
- **Medios de comunicación:** Reportar tendencias reales sin alarmar innecesariamente
- **Individuos:** Evaluar riesgo personal y ajustar precauciones

### 1️⃣1️⃣ Mapa de Calor de Correlación Completo
**Archivo:** `11_mapa_calor_correlacion.png`

**Qué muestra:** Matriz de correlación entre todas las variables numéricas del dataset (casos, muertes, movilidad, fin de semana, feriados).

**Interpretación:**
- **Rojo intenso:** Correlación positiva fuerte (cuando una sube, la otra también)
- **Azul intenso:** Correlación negativa fuerte (cuando una sube, la otra baja)
- **Blanco:** Sin correlación
- Útil para identificar relaciones entre variables y validar hipótesis
- Por ejemplo: casos acumulados y muertes acumuladas tienen correlación cercana a 1 (esperado)

**¿Qué nos dice esta gráfica?**
Este es el "mapa de conexiones" entre todas las variables del dataset. Es una herramienta poderosa para:

**Validar hipótesis:**
- ¿La movilidad realmente afecta los casos? → Ver correlación entre columnas de movilidad y daily_cases
- ¿Los fines de semana afectan reportes? → Ver correlación entre is_weekend y daily_cases

**Descubrir patrones no obvios:**
- Correlaciones inesperadas pueden indicar factores causales ocultos
- Falta de correlación donde esperábamos una puede indicar problemas en los datos

**Cómo leerlo:**
- **Diagonal (1.0):** Cada variable perfectamente correlacionada consigo misma
- **Casos acumulados ↔ Muertes acumuladas (~0.95):** Fuerte correlación (más casos = más muertes)
- **Movilidad residencial ↔ Otros tipos de movilidad (negativa):** Cuando aumenta tiempo en casa, disminuye movilidad externa
- **Daily_cases ↔ Movilidad en comercios (positiva):** Más visitas = más contagios

**Correlaciones importantes a buscar:**
1. **Casos vs Movilidad:** ¿Qué actividades tienen mayor correlación con contagios?
2. **Casos vs Fines de semana:** ¿Hay sesgo de reporte?
3. **Casos vs Días feriados:** ¿Los feriados afectan los datos?

**Utilidad práctica:**
- **Científicos de datos:** Selección de variables para modelos predictivos
- **Epidemiólogos:** Identificar factores de riesgo principales
- **Políticos:** Decidir qué restricciones implementar (enfocar en actividades con alta correlación)
- **Investigadores:** Generar nuevas hipótesis para estudios profundos
- **Verificación de calidad:** Detectar datos anómalos (correlaciones que no tienen sentido)

## Cómo Generar las Figuras

### 1. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 2. Ejecutar el script de visualización

```powershell
python -m Vizualize.plot --input "Output/IntegratedData_cleaned.csv" --outdir "Output/figures"
```

Las 11 figuras se guardarán automáticamente en `Output/figures/`.

## 📈 Casos de Uso Reales

Este proyecto y dataset pueden ser utilizados por:

### 🏥 Sector Salud
- **Hospitales:** Planificar capacidad de UCI y personal según tendencias
- **Departamentos de Salud Pública:** Diseñar campañas de vacunación y comunicación
- **Investigadores médicos:** Estudiar patrones de transmisión y efectividad de tratamientos

### 🏛️ Gobierno y Política Pública
- **Tomadores de decisiones:** Evaluar cuándo implementar/levantar restricciones
- **Planificadores urbanos:** Diseñar ciudades más resilientes a pandemias
- **Gestión de emergencias:** Preparación para futuras crisis sanitarias

### 📚 Educación e Investigación
- **Universidades:** Material didáctico para cursos de epidemiología, ciencia de datos, salud pública
- **Estudiantes:** Proyectos de tesis sobre análisis de datos, machine learning aplicado
- **Investigadores:** Publicaciones académicas sobre correlación movilidad-contagios

### 💼 Sector Empresarial
- **Comercios:** Entender patrones de consumo durante crisis
- **Transporte:** Planificar servicios según demanda real
- **Seguros:** Evaluar riesgos y ajustar primas
- **Empresas tech:** Desarrollar soluciones de monitoreo y predicción

### 📊 Ciencia de Datos y Analytics
- **Modelos predictivos:** Entrenar algoritmos de machine learning para predecir olas
- **Análisis de series temporales:** Estudiar patrones estacionales y cíclicos
- **Visualización de datos:** Ejemplos de buenas prácticas en gráficas explicativas

## 🔍 Insights Principales del Análisis

Después de procesar y visualizar este dataset, podemos concluir:

1. **La movilidad SÍ afecta los contagios:** Existe correlación clara entre aumento en actividades públicas y casos
2. **Las muertes siguen a los casos con 2-3 semanas de retraso:** Patrón consistente útil para predicción
3. **Los datos tienen sesgo de reporte:** Los fines de semana y feriados muestran menos casos (efecto administrativo)
4. **La tasa de mortalidad varía significativamente por región:** No todos los estados experimentaron la misma severidad
5. **El comportamiento social cambió drásticamente:** Las gráficas de movilidad muestran un "antes y después" claro
6. **Los promedios móviles son esenciales:** Los datos diarios crudos tienen demasiado ruido para análisis

## 🛠️ Tecnologías Utilizadas

- **Python 3.x:** Lenguaje de programación principal
- **Pandas:** Manipulación y análisis de datos (lectura por chunks, limpieza, agregaciones)
- **Matplotlib:** Creación de visualizaciones estáticas de alta calidad
- **Seaborn:** Gráficas estadísticas avanzadas (mapas de calor, distribuciones)
- **NumPy:** Operaciones numéricas y álgebra lineal
- **Git/GitHub:** Control de versiones y colaboración

## 📁 Estructura del Proyecto y Explicación de Archivos .py

```
WilsonTrabajo1/
├── 📁 Config/                    # ⚙️ Módulo de configuración
│   ├── __init__.py              # Hace que Config sea un paquete Python
│   └── Config.py                # ⚙️ CONFIGURACIÓN CENTRALIZADA
│
├── 📁 Extract/                   # 📥 Módulo de extracción de datos
│   ├── __init__.py              # Hace que Extract sea un paquete Python
│   ├── Extract.py               # 📥 EXTRACCIÓN DE DATOS
│   └── 📁 Clean/                # 🧹 Submódulo de limpieza
│       ├── __init__.py          # Hace que Clean sea un paquete Python
│       └── Clean.py             # 🧹 LIMPIEZA DE DATOS
│
├── 📁 Transform/                 # 🔄 Módulo de transformación
│   ├── __init__.py              # Hace que Transform sea un paquete Python
│   └── Transform.py             # 🔄 TRANSFORMACIÓN Y ANÁLISIS
│
├── 📁 Load/                      # 💾 Módulo de carga/guardado
│   ├── __init__.py              # Hace que Load sea un paquete Python
│   └── Load.py                  # 💾 PERSISTENCIA DE DATOS
│
├── 📁 Vizualize/                 # 📊 Módulo de visualización
│   ├── __init__.py              # Hace que Vizualize sea un paquete Python
│   └── plot.py                  # 📊 GENERACIÓN DE GRÁFICAS
│
├── 📁 Output/                    # 📂 Archivos de salida
│   ├── __init__.py              # Hace que Output sea un paquete Python
│   ├── IntegratedData_cleaned.csv      # Dataset limpio (77MB)
│   ├── IntegratedData_transformed.csv  # Dataset transformado (generado por pipeline)
│   ├── agregado_nacional.csv           # Agregaciones nacionales
│   ├── top_estados.csv                 # Top 10 estados
│   ├── top_condados.csv                # Top 10 condados
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
├── pipeline.py                  # 🚀 PIPELINE ETL COMPLETO
├── IntegratedData.csv           # Dataset original (77MB)
├── requirements.txt             # Dependencias Python
└── README.md                    # Esta documentación

Total: ~155MB de datos + 11 visualizaciones profesionales
```

### 📝 ¿Para Qué Sirve Cada Archivo .py?

#### ⚙️ **Config/Config.py** - Configuración Centralizada del Proyecto
**Propósito:** Almacena TODAS las configuraciones en un solo lugar para evitar "números mágicos" y facilitar mantenimiento.

**Qué contiene:**
- 📁 **Rutas de directorios:** Define dónde están los datos, salidas y figuras
  ```python
  PROJECT_ROOT = Path(__file__).parent.parent  # Raíz del proyecto
  DATA_DIR = PROJECT_ROOT                      # Donde están los CSV originales
  OUTPUT_DIR = PROJECT_ROOT / "Output"         # Donde se guardan resultados
  FIGURES_DIR = OUTPUT_DIR / "figures"         # Donde se guardan gráficas
  ```

- ⚙️ **Parámetros de procesamiento:**
  ```python
  CHUNK_SIZE = 100_000              # Cuántas filas procesar a la vez (memoria eficiente)
  MOVING_AVERAGE_WINDOW = 7         # Ventana para promedios móviles
  TOP_N_COUNTIES = 10               # Cuántos condados mostrar en rankings
  TOP_N_STATES = 10                 # Cuántos estados mostrar en rankings
  ```

- 📊 **Configuración de visualización:**
  ```python
  FIGURE_SIZE_DEFAULT = (12, 6)     # Tamaño por defecto de gráficas
  DPI = 100                         # Resolución de imágenes
  COLOR_PALETTE = 'Set2'            # Paleta de colores Seaborn
  ```

- 📋 **Definición de columnas esperadas:**
  ```python
  EXPECTED_COLUMNS = ['date', 'county', 'state', 'fips', 'cases', 'deaths', ...]
  MOBILITY_COLUMNS = ['retail_recreation', 'grocery_pharmacy', 'parks', ...]
  NUMERIC_COLUMNS = ['cases', 'deaths', 'daily_cases', 'daily_deaths']
  DATE_COLUMNS = ['date']
  ```

- 🛠️ **Funciones de utilidad:**
  - `ensure_directories()`: Crea los directorios necesarios si no existen
  - `get_config_summary()`: Muestra un resumen de toda la configuración

**Cuándo usarlo:**
- Al inicio de cualquier script para importar configuraciones
- Si necesitas cambiar rutas, tamaños de figura, o parámetros globales
- Para mantener consistencia en todo el proyecto

**Ejemplo de uso:**
```python
from Config.Config import OUTPUT_DIR, CHUNK_SIZE, ensure_directories

ensure_directories()  # Crear directorios si no existen
print(f"Procesando con chunks de {CHUNK_SIZE:,} filas")
```

---

#### 📥 **Extract/Extract.py** - Extracción de Datos desde CSV
**Propósito:** Proporciona múltiples estrategias para leer el dataset según necesidades (memoria, velocidad, filtros).

**Qué contiene:**
Clase `DataExtractor` con 7 métodos diferentes de extracción:

1. **`extract_full()`** - Carga completa en memoria
   - Usa cuando: Tienes suficiente RAM (8GB+) y necesitas todos los datos a la vez
   - Retorna: DataFrame completo de pandas

2. **`extract_chunks(chunk_size)`** - Iterador por chunks
   - Usa cuando: Archivo muy grande (>1GB) y no cabe en memoria
   - Retorna: Generador que produce chunks de datos
   - Ejemplo: Procesar 100,000 filas a la vez

3. **`extract_columns(columns)`** - Solo columnas específicas
   - Usa cuando: Solo necesitas algunas columnas (ahorra memoria)
   - Retorna: DataFrame con columnas seleccionadas

4. **`extract_sample(frac=0.1)`** - Muestreo aleatorio
   - Usa cuando: Quieres hacer pruebas rápidas con 10% de datos
   - Retorna: DataFrame con muestra aleatoria

5. **`extract_by_state(states)`** - Filtrar por estados
   - Usa cuando: Solo necesitas datos de ciertos estados (ej: California, Texas)
   - Retorna: DataFrame filtrado

6. **`extract_date_range(start, end)`** - Filtrar por fechas
   - Usa cuando: Solo necesitas un período específico (ej: marzo-abril 2021)
   - Retorna: DataFrame con fechas en el rango

7. **`get_info()`** - Información del archivo SIN cargarlo
   - Usa cuando: Quieres saber tamaño, columnas, etc. sin usar memoria
   - Retorna: Diccionario con metadatos

**Cuándo usarlo:**
- Al inicio del pipeline para cargar datos originales
- Cuando necesites leer solo parte de los datos
- Para análisis exploratorios rápidos con muestras

**Ejemplo de uso:**
```python
from Extract.Extract import DataExtractor

# Crear extractor
extractor = DataExtractor("IntegratedData.csv")

# Opción 1: Cargar todo (si tienes RAM)
df_completo = extractor.extract_full()

# Opción 2: Procesar por chunks (archivos grandes)
for chunk in extractor.extract_chunks(chunk_size=50000):
    procesar(chunk)  # Procesa cada chunk

# Opción 3: Solo datos de California
df_california = extractor.extract_by_state(['California'])

# Opción 4: Solo columnas de casos y muertes
df_mini = extractor.extract_columns(['date', 'cases', 'deaths'])
```

---

#### 🧹 **Extract/Clean/Clean.py** - Limpieza de Datos
**Propósito:** Limpiar y normalizar datos crudos para análisis (manejo de chunks para archivos grandes).

**Qué hace:**
1. **Normalización de nombres de columnas:**
   - Convierte a minúsculas: `Cases` → `cases`
   - Remueve espacios: `Daily Cases` → `daily_cases`

2. **Limpieza de valores:**
   - Strings: Quita espacios al inicio/final
   - Valores vacíos: Convierte `""` → `NaN`
   - Fechas: Parsea automáticamente columnas `date`

3. **Eliminación de duplicados:**
   - Identifica filas duplicadas
   - Las elimina manteniendo la primera ocurrencia
   - Usa streaming para archivos grandes (no carga todo en memoria)

4. **Eliminación de filas vacías:**
   - Detecta filas donde TODAS las columnas son NaN
   - Las elimina para reducir tamaño del archivo

**Procesamiento por chunks:**
- Lee el archivo en bloques de 100,000 filas
- Procesa cada bloque independientemente
- Guarda resultados de manera incremental
- **Ventaja:** Puede procesar archivos de 10GB+ con solo 2GB de RAM

**Cuándo usarlo:**
- Inmediatamente después de recibir datos crudos
- Antes de cualquier análisis o visualización
- Si el archivo tiene problemas de formato

**Ejemplo de uso:**
```python
from Extract.Clean.Clean import clean_csv

# Limpiar archivo (procesamiento automático por chunks)
clean_csv(
    input_csv="IntegratedData.csv",
    output_csv="Output/IntegratedData_cleaned.csv"
)

# Resultado: Archivo limpio guardado en Output/
```

**Funciones principales:**
- `normalize_column_name(col)`: Normaliza nombre de columna
- `clean_chunk(chunk)`: Limpia un chunk de datos
- `clean_csv(input, output)`: Función principal que orquesta todo

---

#### 🔄 **Transform/Transform.py** - Transformación y Análisis de Datos
**Propósito:** Calcular métricas derivadas, agregaciones y análisis avanzados sobre datos limpios.

**Qué contiene:**
Clase `DataTransformer` con 15+ funciones de transformación:

**1. Métricas Derivadas:**
- `calculate_moving_average(column, window=7)`: Promedio móvil (suaviza series temporales)
- `calculate_growth_rate(column)`: Tasa de crecimiento porcentual diaria
- `calculate_mortality_rate()`: Muertes / Casos * 100

**2. Agregaciones:**
- `aggregate_by_date()`: Suma nacional diaria
- `aggregate_by_state()`: Totales por estado
- `aggregate_by_county()`: Totales por condado

**3. Rankings:**
- `get_top_counties(metric, n=10)`: Top N condados por métrica
- `get_top_states(metric, n=10)`: Top N estados por métrica

**4. Análisis Estadístico:**
- `calculate_correlation_matrix(columns)`: Matriz de correlación
- `get_summary_statistics()`: Estadísticas descriptivas (media, mediana, std, etc.)

**5. Feature Engineering:**
- `add_time_features()`: Agrega año, mes, semana, día, trimestre desde fecha
- `normalize_column(column, method)`: MinMax o Z-score normalización
- `filter_outliers(column, method)`: Detecta y remueve outliers

**Cuándo usarlo:**
- Después de limpiar datos y antes de visualizar
- Para calcular métricas que no están en los datos originales
- Para análisis exploratorio y generación de insights

**Ejemplo de uso:**
```python
from Transform.Transform import DataTransformer
import pandas as pd

# Cargar datos limpios
df = pd.read_csv("Output/IntegratedData_cleaned.csv")

# Crear transformador
transformer = DataTransformer(df)

# Calcular promedio móvil de 7 días para casos
df_transformed = transformer.calculate_moving_average('daily_cases', window=7)

# Calcular tasa de mortalidad
df_transformed = transformer.calculate_mortality_rate()

# Obtener top 10 estados con más casos
top_states = transformer.get_top_states('cases', n=10)

# Agregar características temporales (año, mes, semana, etc.)
df_transformed = transformer.add_time_features()

# Calcular matriz de correlación
corr_matrix = transformer.calculate_correlation_matrix()
```

---

#### 💾 **Load/Load.py** - Persistencia y Carga de Datos
**Propósito:** Guardar y cargar datos procesados en múltiples formatos (CSV, Excel, JSON, Parquet).

**Qué contiene:**
Clase `DataLoader` con funciones de guardado/carga:

**Formatos soportados:**
1. **CSV** - `save_to_csv()` / `load_from_csv()`
   - Formato universal, compatible con todo
   - Opción chunked para archivos grandes

2. **Excel** - `save_to_excel()` / `load_from_excel()`
   - Para reportes y análisis en Excel/Sheets
   - Soporta múltiples hojas

3. **JSON** - `save_to_json()` / `load_from_json()`
   - Para APIs y aplicaciones web
   - Soporta JSON Lines (streaming)

4. **Parquet** - `save_to_parquet()` / `load_from_parquet()`
   - Formato columnar comprimido
   - Más rápido y 70% más pequeño que CSV

**Funciones adicionales:**
- `create_backup(filename)`: Crea copia de seguridad con timestamp
- `save_metadata(filename, metadata)`: Guarda metadatos en JSON
- `load_metadata(filename)`: Carga metadatos
- `list_files(extension)`: Lista archivos en Output/
- `get_file_info(filename)`: Información de archivo (tamaño, fecha, etc.)

**Cuándo usarlo:**
- Al final del pipeline para guardar resultados
- Para crear backups antes de modificaciones
- Para exportar datos a diferentes herramientas

**Ejemplo de uso:**
```python
from Load.Load import DataLoader
import pandas as pd

# Crear loader
loader = DataLoader(output_dir="Output")

# Guardar DataFrame en CSV
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
loader.save_to_csv(df, "resultados.csv")

# Guardar en Excel
loader.save_to_excel(df, "resultados.xlsx", sheet_name="Datos")

# Guardar en Parquet (comprimido)
loader.save_to_parquet(df, "resultados.parquet", compression='snappy')

# Crear backup
loader.create_backup("IntegratedData_cleaned.csv")

# Guardar metadatos
metadata = {
    'descripcion': 'Datos procesados',
    'filas': len(df),
    'columnas': list(df.columns)
}
loader.save_metadata("resultados.csv", metadata)

# Cargar datos
df_cargado = loader.load_from_csv("resultados.csv")

# Listar todos los CSV en Output/
archivos = loader.list_files(extension='.csv')
print(f"Encontrados {len(archivos)} archivos CSV")
```

---

#### 📊 **Vizualize/plot.py** - Generación de Visualizaciones
**Propósito:** Crear 11 gráficas profesionales en español que explican la pandemia desde múltiples ángulos.

**Qué contiene:**
11 funciones especializadas de visualización:

1. **`plot_1_temporal_nacional()`** - Evolución temporal de casos y muertes
   - Gráfica de líneas con doble eje Y
   - Muestra tendencias nacionales día a día

2. **`plot_2_top_condados()`** - Top 10 condados con más casos
   - Gráfica de barras horizontales
   - Identifica hotspots locales

3. **`plot_3_casos_vs_muertes()`** - Relación casos vs muertes
   - Scatter plot con regresión
   - Muestra tasa de letalidad

4. **`plot_4_movilidad_correlacion()`** - Impacto de movilidad en casos
   - Gráfica de barras de correlaciones
   - Identifica qué actividades aumentan contagios

5. **`plot_5_comparacion_dias()`** - Días laborales vs fines de semana
   - Gráfica de barras comparativa
   - Muestra sesgos de reporte

6. **`plot_6_top_estados_casos()`** - Top 10 estados más afectados
   - Gráfica de barras horizontales
   - Comparación a nivel estatal

7. **`plot_7_tasa_mortalidad_estados()`** - Tasa de mortalidad por estado
   - Gráfica de barras con gradiente de color
   - Identifica estados con mayor severidad

8. **`plot_8_evolucion_movilidad()`** - Evolución de movilidad en el tiempo
   - Gráfica de líneas múltiples
   - Muestra cambios de comportamiento

9. **`plot_9_casos_dia_semana()`** - Distribución por día de la semana
   - Gráfica de barras por día
   - Identifica patrones semanales

10. **`plot_10_promedio_movil()`** - Promedio móvil de casos (7 días)
    - Gráfica con datos crudos + suavizados
    - Facilita ver tendencias reales

11. **`plot_11_mapa_calor_correlacion()`** - Mapa de calor de correlaciones
    - Heatmap con todas las variables
    - Identifica relaciones entre variables

**Características comunes:**
- Todas en español (títulos, etiquetas, leyendas)
- Estilo profesional consistente
- Alta resolución (DPI 100)
- Colores accesibles (colorblind-friendly)
- Guardado automático en PNG

**Cuándo usarlo:**
- Al final del pipeline para crear reportes visuales
- Para presentaciones y reportes
- Para exploración de datos

**Ejemplo de uso:**
```python
from Vizualize.plot import (
    plot_1_temporal_nacional,
    plot_11_mapa_calor_correlacion,
    generate_all_plots
)
import pandas as pd

# Cargar datos
df = pd.read_csv("Output/IntegratedData_cleaned.csv")

# Generar una gráfica específica
plot_1_temporal_nacional(df, outdir="Output/figures")

# O generar todas las 11 gráficas de una vez
generate_all_plots(df, outdir="Output/figures")

# Las gráficas se guardan automáticamente en Output/figures/
```

---

#### 🚀 **pipeline.py** - Pipeline ETL Completo Integrador
**Propósito:** Orquesta TODO el flujo de trabajo de principio a fin (Extract → Clean → Transform → Load → Visualize).

**Qué hace:**
Clase `COVIDPipeline` que ejecuta 5 pasos secuenciales:

**PASO 1: Extracción** (`step1_extract`)
- Lee el archivo CSV original
- Valida que existe
- Puede usar diferentes métodos (full, chunks, sample)

**PASO 2: Limpieza** (`step2_clean`)
- Ejecuta `clean_csv()` con procesamiento por chunks
- Normaliza columnas
- Elimina duplicados y valores vacíos
- Guarda: `IntegratedData_cleaned.csv`

**PASO 3: Transformación** (`step3_transform`)
- Calcula promedios móviles (7 días)
- Calcula tasa de mortalidad
- Calcula tasa de crecimiento
- Agrega características temporales (año, mes, semana, etc.)
- Retorna: DataFrame con métricas derivadas

**PASO 4: Carga** (`step4_load`)
- Guarda datos transformados en CSV
- Crea archivo de metadatos JSON
- Crea backup del archivo limpio
- Guarda: `IntegratedData_transformed.csv` + metadatos

**PASO 5: Análisis y Agregaciones** (`step5_analyze`)
- Agrega datos a nivel nacional
- Identifica top 10 estados
- Identifica top 10 condados
- Calcula estadísticas descriptivas
- Calcula matriz de correlación
- Guarda: `agregado_nacional.csv`, `top_estados.csv`, `top_condados.csv`

**Cuándo usarlo:**
- Para ejecutar el análisis completo de principio a fin
- En producción o automatización
- Para procesar nuevos datasets con la misma estructura

**Ejemplo de uso:**
```bash
# Ejecutar pipeline completo con configuración por defecto
python pipeline.py

# Ver configuración antes de ejecutar
python pipeline.py --show-config

# Usar un archivo de entrada diferente
python pipeline.py --input OtroDatos.csv

# No guardar archivos intermedios (solo resultado final)
python pipeline.py --skip-intermediate
```

**Desde Python:**
```python
from pipeline import COVIDPipeline

# Crear pipeline
pipeline = COVIDPipeline(input_file="IntegratedData.csv")

# Ejecutar pipeline completo
df_final = pipeline.run_full_pipeline(save_intermediate=True)

# O ejecutar pasos individuales
df_clean = pipeline.step2_clean()
df_transformed = pipeline.step3_transform(df_clean)
pipeline.step4_load(df_transformed)
results = pipeline.step5_analyze(df_transformed)

print(f"✅ Pipeline completado: {len(df_final):,} filas procesadas")
```

**Salida del pipeline:**
- `IntegratedData_cleaned.csv` - Datos limpios
- `IntegratedData_transformed.csv` - Datos con métricas derivadas
- `agregado_nacional.csv` - Suma nacional diaria
- `top_estados.csv` - Top 10 estados
- `top_condados.csv` - Top 10 condados
- Archivo de metadatos JSON
- Backup con timestamp

---

### 🔄 Flujo de Trabajo Completo

```
1. IntegratedData.csv (77MB)
         ↓
2. Config.py (carga configuraciones)
         ↓
3. Extract.py (lee datos)
         ↓
4. Clean.py (limpia datos)
         ↓
5. Transform.py (calcula métricas)
         ↓
6. Load.py (guarda resultados)
         ↓
7. plot.py (genera gráficas)
         ↓
8. Output/ (11 PNG + CSVs procesados)
```

**Todo esto es orquestado por `pipeline.py`** para ejecutar de forma automática.

---

### 💡 Consejos de Uso

**Para análisis exploratorio rápido:**
```python
# Usar Extract.py con muestreo
from Extract.Extract import DataExtractor
extractor = DataExtractor("IntegratedData.csv")
df_sample = extractor.extract_sample(frac=0.1)  # Solo 10% de datos
```

**Para procesar archivos gigantes (>5GB):**
```python
# Usar procesamiento por chunks
from Extract.Extract import DataExtractor
for chunk in DataExtractor("BigFile.csv").extract_chunks(50000):
    process(chunk)  # Procesa de a poco
```

**Para crear reportes automatizados:**
```bash
# Ejecutar pipeline completo desde terminal
python pipeline.py --input NuevosDatos.csv
```

**Para análisis específico de un estado:**
```python
from Extract.Extract import DataExtractor
df_california = DataExtractor("IntegratedData.csv").extract_by_state(['California'])
```

Total: ~155MB de datos + 11 visualizaciones profesionales + Pipeline ETL completo

---

## 📊 Resumen Visual: Arquitectura del Proyecto

```
┌─────────────────────────────────────────────────────────────────┐
│                    PROYECTO WILSONTRABAJO1                      │
│          Análisis de COVID-19 y Movilidad en EE.UU.            │
└─────────────────────────────────────────────────────────────────┘

                         📥 ENTRADA
                             │
                   IntegratedData.csv
                    (77MB, 935k filas)
                             │
         ┌───────────────────┴───────────────────┐
         │                                       │
         ▼                                       ▼
    ⚙️ Config.py                          📥 Extract.py
    • Rutas                                • 7 métodos de
    • Parámetros                            extracción
    • Constantes                           • Filtros por estado
    │                                      • Muestreo aleatorio
    │                                           │
    │                                           ▼
    │                                    🧹 Clean.py
    │                                    • Procesamiento chunks
    │                                    • Normalización
    │                                    • Deduplicación
    │                                           │
    └────────────┬──────────────────────────────┘
                 │
                 ▼
          🔄 Transform.py
          • Promedios móviles
          • Tasas derivadas
          • Agregaciones
          • Correlaciones
          • 15+ funciones
                 │
                 ▼
          💾 Load.py
          • Guardar CSV/Excel
          • Guardar JSON/Parquet
          • Metadatos
          • Backups
                 │
         ┌───────┴───────┐
         │               │
         ▼               ▼
  📊 Vizualize.py   📂 Output/
  • 11 gráficas     • IntegratedData_cleaned.csv (77MB)
    en español      • IntegratedData_transformed.csv
  • Profesionales   • agregado_nacional.csv
  • PNG alta res    • top_estados.csv
         │          • top_condados.csv
         │          • metadatos.json
         └───────┬──┘
                 │
                 ▼
          📁 Output/figures/
          ┌──────────────────────────────────────┐
          │ ✅ 1_evolucion_casos_muertes.png    │
          │ ✅ 2_top_condados_casos.png         │
          │ ✅ 3_casos_vs_muertes.png           │
          │ ✅ 4_movilidad_correlacion.png      │
          │ ✅ 5_comparacion_dias.png           │
          │ ✅ 6_top_estados_casos.png          │
          │ ✅ 7_tasa_mortalidad_estados.png    │
          │ ✅ 8_evolucion_movilidad.png        │
          │ ✅ 9_casos_dia_semana.png           │
          │ ✅ 10_promedio_movil.png            │
          │ ✅ 11_mapa_calor_correlacion.png    │
          └──────────────────────────────────────┘

         TODO ORQUESTADO POR: 🚀 pipeline.py
         Ejecutar: python pipeline.py
```

### 🎯 Flujo de Datos Simplificado

```
CSV Crudo → Extract → Clean → Transform → Load → Visualize → Resultados
  (77MB)      (lee)   (limpia)  (calcula)  (guarda)  (grafica)   (11 PNG)
```

### 📈 Métricas del Proyecto

| Componente | Líneas de Código | Funciones | Descripción |
|------------|------------------|-----------|-------------|
| **Config.py** | 290 | 2 | Configuración centralizada |
| **Extract.py** | 250 | 8 | Extracción de datos |
| **Clean.py** | 130 | 3 | Limpieza de datos |
| **Transform.py** | 450 | 16 | Transformaciones y análisis |
| **Load.py** | 450 | 13 | Persistencia de datos |
| **plot.py** | 620 | 12 | Visualizaciones profesionales |
| **pipeline.py** | 280 | 6 | Orquestador ETL completo |
| **TOTAL** | **2,470** | **60** | **Pipeline ETL completo funcional** |

### 📦 Archivos Generados por el Pipeline

| Archivo | Tamaño | Filas | Columnas | Descripción |
|---------|--------|-------|----------|-------------|
| IntegratedData_cleaned.csv | 77MB | 935,444 | 17 | Datos limpios |
| IntegratedData_transformed.csv | 85MB | 935,444 | 25+ | + métricas derivadas |
| agregado_nacional.csv | 50KB | 365 | 4 | Suma nacional diaria |
| top_estados.csv | 2KB | 10 | 5 | Top 10 estados |
| top_condados.csv | 3KB | 10 | 6 | Top 10 condados |
| 11 gráficas PNG | 5MB | - | - | Visualizaciones profesionales |

---

## 🚀 Próximas Mejoras Posibles

- [ ] Implementar análisis interactivo con Plotly/Dash
- [ ] Crear dashboard web en tiempo real
- [ ] Agregar mapas geográficos con Folium
- [ ] Modelos de machine learning para predicción de casos
- [ ] API REST para consultar datos
- [ ] Análisis de sentimiento en redes sociales correlacionado con casos
- [ ] Comparación internacional (agregar datos de otros países)
- [ ] Análisis de variantes del virus
- [ ] Estudio de efectividad de vacunas por región

## 👥 Contribuciones

Este proyecto fue desarrollado como parte del curso de Ciencia de Datos. 

¿Quieres contribuir? Las pull requests son bienvenidas. Para cambios mayores, por favor abre un issue primero para discutir qué te gustaría cambiar.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para fines educativos y de investigación.

## 📧 Contacto

**Repositorio:** [WilsonTrabajo1](https://github.com/kenmaroyert1/WilsonTrabajo1)  
**Rama principal de desarrollo:** `feature1`

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub

**Última actualización:** Febrero 2026
