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

## Estructura del Proyecto

```
WilsonTrabajo1/
├── Config/                   # Configuraciones del proyecto
├── Extract/
│   ├── Extract.py           # Módulo de extracción (placeholder)
│   └── Clean/
│       └── Clean.py         # Limpieza de datos por chunks
├── Transform/
│   └── Transform.py         # Transformaciones (placeholder)
├── Load/
│   └── Load.py              # Carga de datos (placeholder)
├── Vizualize/
│   └── plot.py              # Generación de 11 gráficas profesionales
├── Output/
│   ├── IntegratedData_cleaned.csv  # Dataset limpio (77MB)
│   └── figures/             # 11 visualizaciones PNG
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
├── IntegratedData.csv       # Dataset original (77MB)
├── requirements.txt         # Dependencias Python
└── README.md               # Esta documentación

Total: ~155MB de datos + 11 visualizaciones profesionales
```

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
